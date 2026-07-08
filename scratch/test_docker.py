import os
import subprocess

print("DOCKER_HOST in python os.environ:", os.environ.get("DOCKER_HOST"))
try:
    res = subprocess.run(["docker", "info"], capture_output=True, text=True, check=True)
    print("docker info succeeded!")
except Exception as e:
    print("docker info failed:", e)
    if hasattr(e, "stderr"):
        print("stderr:", e.stderr)
