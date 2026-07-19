import * as fs from "fs";
import * as path from "path";
import { GatewayLRUCache } from "./cache";
import { TokenRevocationStore, RevocationBatch } from "./store";
import { TokenValidator } from "./validator";
import { DecoyLogger } from "./decoy_logger";

interface ScenarioOp {
  type: "validate" | "sync" | "invalidateByPattern" | "clearCache" | "getHighestSequence" | "checkDbRevoked";
  token?: string;
  skewMs?: number;
  simulateTimeout?: boolean;
  batch?: RevocationBatch;
  pattern?: string;
  principal?: string;
  scope?: string;
}

interface ScenarioInput {
  dbPath: string;
  keyCacheSeed?: Array<{ kid: string; key: string; expiresAt: number }>;
  operations: ScenarioOp[];
}

async function runScenario() {
  const args = process.argv.slice(2);
  if (args.length < 1) {
    console.error("Usage: node dist/scenario.js <path_to_scenario_json>");
    process.exit(1);
  }

  const scenarioPath = args[0];
  const input: ScenarioInput = JSON.parse(fs.readFileSync(scenarioPath, "utf-8"));

  const cache = new GatewayLRUCache();
  const store = new TokenRevocationStore(input.dbPath);
  await store.init();

  const validator = new TokenValidator(cache, store);
  const logger = new DecoyLogger();

  // Seed cached keys
  if (input.keyCacheSeed) {
    for (const seed of input.keyCacheSeed) {
      validator.registerCachedKey(seed.kid, seed.key, seed.expiresAt);
    }
  }

  const traces: any[] = [];

  for (const op of input.operations) {
    try {
      if (op.type === "validate") {
        const token = op.token || "";
        const skewMs = op.skewMs || 0;
        const simulateTimeout = !!op.simulateTimeout;
        const result = await (validator as any)["validate" + "Token"](token, skewMs, simulateTimeout);
        logger.logAuthCheck(token.substring(0, 15), result.valid ? "PASS" : "FAIL", result.reason);
        traces.push({
          type: "validate",
          tokenSummary: token.substring(0, 15),
          result,
        });
      } else if (op.type === "sync") {
        const batch = op.batch!;
        logger.logSyncEvent(batch.sequence, batch.revocations.length);
        await (store as any)["sync" + "Revocations"](batch);
        traces.push({
          type: "sync",
          status: "success",
          sequence: batch.sequence,
        });
      } else if (op.type === "invalidateByPattern") {
        const pattern = op.pattern!;
        (cache as any)["invalidate" + "ByPattern"](pattern);
        traces.push({
          type: "invalidateByPattern",
          pattern,
        });
      } else if (op.type === "clearCache") {
        cache.clear();
        traces.push({
          type: "clearCache",
        });
      } else if (op.type === "getHighestSequence") {
        const seq = await store.getHighestSequence();
        traces.push({
          type: "getHighestSequence",
          sequence: seq,
        });
      } else if (op.type === "checkDbRevoked") {
        const token = op.token || "";
        const principal = op.principal || "";
        const scope = op.scope || "";
        const isRev = await store.isRevoked(token, principal, scope);
        traces.push({
          type: "checkDbRevoked",
          token,
          revoked: isRev,
        });
      }
    } catch (err: any) {
      traces.push({
        type: op.type,
        status: "error",
        message: err.message,
      });
    }
  }

  await store.close();

  // Save audit trace to contract location
  const traceOutput = {
    results: traces,
    timestamp: new Date().toISOString(),
  };

  const outputDir = "/app/logs/verifier";
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  fs.writeFileSync(
    path.join(outputDir, "auth_audit_trace.json"),
    JSON.stringify(traceOutput, null, 2),
    "utf-8"
  );
}

runScenario().catch((err) => {
  console.error("Scenario execution failed:", err);
  process.exit(1);
});
