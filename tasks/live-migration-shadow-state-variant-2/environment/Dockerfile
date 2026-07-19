FROM ubuntu:24.04@sha256:c4a8d5503dfb2a3eb8ab5f807da5bc69a85730fb49b5cfca2330194ebcc41c7b

# terminus-2 agent harness requires tmux + asciinema in the image (not at verifier runtime).
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    asciinema=2.4.0-1 \
    bash=5.2.21-2ubuntu4 \
    g++=4:13.2.0-7ubuntu1 \
    make=4.3-4.1build2 \
    python3=3.12.3-0ubuntu2.1 \
    python3-pip=24.0+dfsg-1ubuntu1.3 \
    python3-venv=3.12.3-0ubuntu2.1 \
    libssl-dev=3.0.13-0ubuntu3.9 \
    ca-certificates=20240203 \
    tmux=3.4-1ubuntu0.1 \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/verifier \
    && /opt/verifier/bin/pip install --no-cache-dir pytest==8.4.1 pytest-json-ctrf==0.3.5

ENV PATH="/opt/verifier/bin:${PATH}"

WORKDIR /app
COPY . /app/environment
RUN chmod +x /app/environment/mig_exec /app/environment/app/tools/inspect.sh
