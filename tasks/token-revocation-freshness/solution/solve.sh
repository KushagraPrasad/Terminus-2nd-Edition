#!/bin/bash
# Writes corrected source files into the gateway environment and compiles them.

cat > environment/src/cache.ts << 'EOF'
import * as jwt from "jsonwebtoken";

interface CacheEntry {
  value: any;
  expiresAt: number;
  principal: string;
  scope: string;
}

export class GatewayLRUCache {
  private cache = new Map<string, CacheEntry>();
  private maxItems: number;
  private defaultTtlMs: number;

  constructor(maxItems: number = 1000, defaultTtlMs: number = 60000) {
    this.maxItems = maxItems;
    this.defaultTtlMs = defaultTtlMs;
  }

  public get(token: string): any | null {
    const entry = this.cache.get(token);
    if (!entry) return null;

    if (Date.now() > entry.expiresAt) {
      this.cache.delete(token);
      return null;
    }

    // Refresh LRU order
    this.cache.delete(token);
    this.cache.set(token, entry);
    return entry.value;
  }

  public set(token: string, value: any): void {
    if (this.cache.has(token)) {
      this.cache.delete(token);
    } else if (this.cache.size >= this.maxItems) {
      // Evict oldest item (first key in map iterator)
      const oldestKey = this.cache.keys().next().value;
      if (oldestKey !== undefined) {
        this.cache.delete(oldestKey);
      }
    }

    let principal = "";
    let scope = "";

    try {
      const decoded = jwt.decode(token) as any;
      if (decoded) {
        principal = decoded.sub || "";
        scope = decoded.scope || "";
      }
    } catch {
      // Ignore decode errors for invalid tokens
    }

    this.cache.set(token, {
      value,
      expiresAt: Date.now() + this.defaultTtlMs,
      principal,
      scope,
    });
  }

  // Invalidate cache records matching pattern
  public invalidateByPattern(pattern: string): void {
    if (pattern.startsWith("principal:") || pattern.startsWith("scope:")) {
      const parts = pattern.split(":");
      const field = parts[0];
      const rule = parts.slice(1).join(":");

      const toDelete: string[] = [];
      for (const [token, entry] of this.cache.entries()) {
        const valToMatch = field === "principal" ? entry.principal : entry.scope;
        if (this.matchWildcard(valToMatch, rule)) {
          toDelete.push(token);
        }
      }
      for (const key of toDelete) {
        this.cache.delete(key);
      }
    } else {
      if (this.cache.has(pattern)) {
        this.cache.delete(pattern);
      }
    }
  }

  private matchWildcard(str: string, rule: string): boolean {
    if (rule === "*") return true;
    if (!rule.includes("*")) return str === rule;
    const escaped = rule.replace(/([.+?^=!:${}()|\[\]\/\\])/g, "\\$1");
    const regex = new RegExp("^" + escaped.split("*").join(".*") + "$");
    return regex.test(str);
  }

  public clear(): void {
    this.cache.clear();
  }

  public get size(): number {
    return this.cache.size;
  }
}
EOF

cat > environment/src/store.ts << 'EOF'
import * as sqlite3 from "sqlite3";
import { promisify } from "util";

export interface RevocationRecord {
  id: string;
  principal: string;
  scope: string;
  timestamp: number;
}

export interface RevocationBatch {
  sequence: number;
  revocations: RevocationRecord[];
}

export class TokenRevocationStore {
  private db: sqlite3.Database;

  constructor(dbPath: string) {
    this.db = new sqlite3.Database(dbPath);
  }

  public async init(): Promise<void> {
    const run: any = promisify(this.db.run.bind(this.db));
    await run(`
      CREATE TABLE IF NOT EXISTS revocations (
        id TEXT PRIMARY KEY,
        principal TEXT,
        scope TEXT,
        timestamp INTEGER,
        sequence INTEGER
      )
    `);
    await run(`
      CREATE TABLE IF NOT EXISTS metadata (
        key TEXT PRIMARY KEY,
        value TEXT
      )
    `);
  }

  public async close(): Promise<void> {
    return new Promise((resolve, reject) => {
      this.db.close((err) => {
        if (err) reject(err);
        else resolve();
      });
    });
  }

  public async getHighestSequence(): Promise<number> {
    const get = promisify(this.db.get.bind(this.db));
    try {
      const row = await get("SELECT value FROM metadata WHERE key = 'highest_sequence'") as any;
      return row ? parseInt(row.value, 10) : -1;
    } catch {
      return -1;
    }
  }

  public async setHighestSequence(seq: number): Promise<void> {
    const run: any = promisify(this.db.run.bind(this.db));
    await run(
      "INSERT OR REPLACE INTO metadata (key, value) VALUES ('highest_sequence', ?)",
      seq.toString()
    );
  }

  // Synchronize batch transaction
  public async syncRevocations(batch: RevocationBatch): Promise<void> {
    const run: any = promisify(this.db.run.bind(this.db));

    const currentSeq = await this.getHighestSequence();
    if (batch.sequence <= currentSeq) {
      throw new Error(`Monotonic sequence violation: batch sequence ${batch.sequence} <= current highest ${currentSeq}`);
    }

    await run("BEGIN TRANSACTION");

    try {
      for (const rec of batch.revocations) {
        if (rec.id === "trigger-crash-sig") {
          throw new Error("Simulated system crash during DB write batch");
        }

        await run(
          `INSERT OR REPLACE INTO revocations (id, principal, scope, timestamp, sequence)
           VALUES (?, ?, ?, ?, ?)`,
          rec.id,
          rec.principal,
          rec.scope,
          rec.timestamp,
          batch.sequence
        );
      }
      await this.setHighestSequence(batch.sequence);
      await run("COMMIT");
    } catch (err) {
      await run("ROLLBACK");
      throw err;
    }
  }

  public async isRevoked(
    tokenId: string,
    principal: string,
    scope: string
  ): Promise<boolean> {
    const all = promisify(this.db.all.bind(this.db));
    try {
      const rows = await all("SELECT id, principal, scope FROM revocations") as any[];
      for (const row of rows) {
        if (row.id === tokenId) {
          return true;
        }

        if (this.matchWildcardPattern(principal, row.principal) &&
            this.matchWildcardPattern(scope, row.scope)) {
          return true;
        }
      }
      return false;
    } catch {
      return false;
    }
  }

  private matchWildcardPattern(value: string, pattern: string): boolean {
    if (pattern === "*") return true;
    if (!pattern.includes("*")) return value === pattern;
    const escaped = pattern.replace(/([.+?^=!:${}()|\[\]\/\\])/g, "\\$1");
    const regex = new RegExp("^" + escaped.split("*").join(".*") + "$");
    return regex.test(value);
  }
}
EOF

cat > environment/src/validator.ts << 'EOF'
import * as jwt from "jsonwebtoken";
import { GatewayLRUCache } from "./cache";
import { TokenRevocationStore } from "./store";
import { JwkFetcher } from "./jwks";

export interface AuthResult {
  valid: boolean;
  reason?: string;
  principal?: string;
  scope?: string;
}

export class TokenValidator {
  private cache: GatewayLRUCache;
  private store: TokenRevocationStore;
  private jwkFetcher: JwkFetcher;
  private keyCache = new Map<string, { key: string; expiresAt: number }>();

  constructor(
    cache: GatewayLRUCache,
    store: TokenRevocationStore,
    jwkFetcher: JwkFetcher = new JwkFetcher()
  ) {
    this.cache = cache;
    this.store = store;
    this.jwkFetcher = jwkFetcher;
  }

  public registerCachedKey(kid: string, key: string, expiresAt: number): void {
    this.keyCache.set(kid, { key, expiresAt });
  }

  private getSkewAdjustedTime(skewMs: number): number {
    return Date.now() + skewMs;
  }

  public async validateToken(
    token: string,
    skewMs: number,
    simulateTimeout: boolean = false
  ): Promise<AuthResult> {
    const cachedResult = this.cache.get(token);
    if (cachedResult !== null) {
      return cachedResult;
    }

    try {
      const decodedHeader = jwt.decode(token, { complete: true }) as any;
      if (!decodedHeader || !decodedHeader.header || !decodedHeader.header.kid) {
        return { valid: false, reason: "Invalid token header structure" };
      }

      const kid = decodedHeader.header.kid;
      let verifyKey = "";

      try {
        verifyKey = await this.jwkFetcher.fetchJwkFromEndpoint(kid, simulateTimeout);
        this.keyCache.set(kid, { key: verifyKey, expiresAt: Date.now() + 3600000 });
      } catch (err) {
        const cached = this.keyCache.get(kid);
        if (!cached) {
          return { valid: false, reason: "JWKS connection failed and no cached key found" };
        }

        if (Date.now() > cached.expiresAt) {
          return { valid: false, reason: "JWKS connection failed and cached fallback key has expired" };
        }
        
        verifyKey = cached.key;
      }

      const payload = jwt.verify(token, verifyKey) as any;
      const principal = payload.sub || "";
      const scope = payload.scope || "";
      const jti = payload.jti || "";

      const validationTime = this.getSkewAdjustedTime(skewMs); 
      if (payload.exp && validationTime > payload.exp * 1000) {
        return { valid: false, reason: "Token validation expired" };
      }

      const isBlacklisted = await this.store.isRevoked(jti, principal, scope);
      if (isBlacklisted) {
        this.cache.invalidateByPattern(token);
        return { valid: false, reason: "Token revoked" };
      }

      const successResult: AuthResult = {
        valid: true,
        principal,
        scope,
      };

      this.cache.set(token, successResult);
      return successResult;
    } catch (err: any) {
      return { valid: false, reason: err.message || "Authorization failed" };
    }
  }
}
EOF

cd environment
npm run build
