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

  // Apply sync batch updates
  public async syncRevocations(batch: RevocationBatch): Promise<void> {
    const run: any = promisify(this.db.run.bind(this.db));

    await this.setHighestSequence(batch.sequence);

    for (const rec of batch.revocations) {
      // Simulate crash hook for testing transaction atomicity
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
  }

  public async isRevoked(
    tokenId: string,
    principal: string,
    scope: string
  ): Promise<boolean> {
    const all = promisify(this.db.all.bind(this.db));
    try {
      // Find all revocations
      const rows = await all("SELECT id, principal, scope FROM revocations") as any[];
      for (const row of rows) {
        if (row.id === tokenId) {
          return true;
        }

        // Wildcard matching helper
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
