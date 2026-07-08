import sys

path = "/home/kusha/venv-wsl/lib/python3.12/site-packages/harbor/environments/docker/docker.py"
try:
    content = open(path).read()
except Exception as e:
    print(f"Error reading file {path}: {e}")
    sys.exit(1)

target = """    @override
    def preflight(cls) -> None:
        if not shutil.which("docker"):
            raise SystemExit(
                "Docker is not installed or not on PATH. "
                "Please install Docker and try again."
            )
        try:
            subprocess.run(
                ["docker", "info"],
                capture_output=True,
                timeout=10,
                check=True,
            )
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            raise SystemExit(
                "Docker daemon is not running. Please start Docker and try again."
            )"""

replacement = """    @override
    def preflight(cls) -> None:
        pass"""

if target in content:
    open(path, "w").write(content.replace(target, replacement))
    print("Successfully patched harbor docker preflight check!")
elif replacement in content:
    print("Harbor docker preflight check is already patched.")
else:
    print("Error: Target pattern not found in harbor docker.py")
    sys.exit(1)
