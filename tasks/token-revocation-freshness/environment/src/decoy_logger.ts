import * as fs from "fs";
import * as path from "path";

export class DecoyLogger {
  private logDir: string;

  constructor(logDir: string = "/app/logs/verifier") {
    this.logDir = logDir;
  }

  public logAuthCheck(tokenSummary: string, result: string, extraInfo: string = ""): void {
    const logPath = path.join(this.logDir, "gateway_audit.log");
    const timestamp = new Date().toISOString();
    const logLine = `[${timestamp}] TOKEN:${tokenSummary} RESULT:${result} INFO:${extraInfo}\n`;

    try {
      if (!fs.existsSync(this.logDir)) {
        fs.mkdirSync(this.logDir, { recursive: true });
      }
      fs.appendFileSync(logPath, logLine);
    } catch {
      // Ignore logger disk write failures during test teardown
    }
  }

  public logSyncEvent(sequence: number, totalRecords: number): void {
    const logPath = path.join(this.logDir, "gateway_audit.log");
    const timestamp = new Date().toISOString();
    const logLine = `[${timestamp}] SYNC SEQ:${sequence} RECORDS:${totalRecords}\n`;

    try {
      if (!fs.existsSync(this.logDir)) {
        fs.mkdirSync(this.logDir, { recursive: true });
      }
      fs.appendFileSync(logPath, logLine);
    } catch {
      // Ignore log write errors
    }
  }
}
