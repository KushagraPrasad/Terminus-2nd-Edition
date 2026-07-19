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

  public async validateToken(
    token: string,
    skewMs: number,
    simulateTimeout: boolean = false
  ): Promise<AuthResult> {
    // 1. Fast-path: check LRU Cache
    const cachedResult = this.cache.get(token);
    if (cachedResult !== null) {
      return cachedResult;
    }

    try {
      // Decode JWT headers to find kid
      const decodedHeader = jwt.decode(token, { complete: true }) as any;
      if (!decodedHeader || !decodedHeader.header || !decodedHeader.header.kid) {
        return { valid: false, reason: "Invalid token header structure" };
      }

      const kid = decodedHeader.header.kid;
      let verifyKey = "";

      try {
        // Fetch from JWKS endpoint
        verifyKey = await this.jwkFetcher.fetchJwkFromEndpoint(kid, simulateTimeout);
        // Cache the retrieved key with a 1-hour expiration
        this.keyCache.set(kid, { key: verifyKey, expiresAt: Date.now() + 3600000 });
      } catch (err) {
        // Fallback to cache
        const cached = this.keyCache.get(kid);
        if (!cached) {
          return { valid: false, reason: "JWKS connection failed and no cached key found" };
        }

        verifyKey = cached.key;
      }

      // 2. Cryptographic signature check
      const payload = jwt.verify(token, verifyKey) as any;
      const principal = payload.sub || "";
      const scope = payload.scope || "";
      const jti = payload.jti || "";

      // 3. Expiration checks with skew offset compensation
      const validationTime = Date.now(); 
      if (payload.exp && validationTime > payload.exp * 1000) {
        return { valid: false, reason: "Token validation expired" };
      }

      // 4. DB Blacklist check
      const isBlacklisted = await this.store.isRevoked(jti, principal, scope);
      if (isBlacklisted) {
        // Remove from memory cache just in case
        this.cache.invalidateByPattern(token);
        return { valid: false, reason: "Token revoked" };
      }

      const successResult: AuthResult = {
        valid: true,
        principal,
        scope,
      };

      // Add to memory cache
      this.cache.set(token, successResult);
      return successResult;
    } catch (err: any) {
      return { valid: false, reason: err.message || "Authorization failed" };
    }
  }
}
