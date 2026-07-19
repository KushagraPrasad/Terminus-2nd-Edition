#!/usr/bin/env python3
import subprocess
import sys
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("task_dir")
    parser.add_argument("--count", type=int, default=20)
    args = parser.parse_args()

    print(f"Starting stress test for {args.task_dir} (running {args.count} trials sequentially)...")
    for i in range(1, args.count + 1):
        print(f"--- Trial {i}/{args.count} ---")
        import os
        my_env = os.environ.copy()
        my_env["PYTHONPATH"] = "."
        res = subprocess.run(
            [sys.executable, "scripts/harbor_gate.py", args.task_dir, "--oracle"],
            capture_output=True,
            text=True,
            env=my_env
        )
        if res.returncode != 0 or "PASS" not in res.stdout:
            print(f"Trial {i} FAILED!")
            print("STDOUT:")
            print(res.stdout)
            print("STDERR:")
            print(res.stderr)
            sys.exit(1)
        print(f"Trial {i} PASSED.")
        import time
        time.sleep(10)
    print(f"Success: All {args.count} trials passed successfully!")

if __name__ == "__main__":
    main()
