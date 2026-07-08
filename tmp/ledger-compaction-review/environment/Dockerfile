FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim@sha256:847b5e690018bc6b9d97a0848da65f721b785f1e78d9c7067b8947c7010b2718

# terminus-2 agent harness requires tmux + asciinema in the image (not at verifier runtime).
WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends asciinema=2.2.0-1 golang-go=2:1.19~1 make=4.3-4.1 tmux=3.3a-3 \
    && rm -rf /var/lib/apt/lists/*

RUN uv pip install --system pytest==8.4.1 pytest-json-ctrf==0.3.5 pytest-randomly==3.16.0

COPY . /app/environment

WORKDIR /app
RUN cd /app/environment && go test ./...
