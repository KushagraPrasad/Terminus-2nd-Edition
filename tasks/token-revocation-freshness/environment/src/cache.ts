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

  // Evict exact match only
  public invalidateByPattern(pattern: string): void {
    if (this.cache.has(pattern)) {
      this.cache.delete(pattern);
    }
  }

  public clear(): void {
    this.cache.clear();
  }

  public get size(): number {
    return this.cache.size;
  }
}
