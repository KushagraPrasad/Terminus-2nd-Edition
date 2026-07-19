FROM rust:1.84-bookworm@sha256:738ae99a3d75623f41e6882566b4ef37e38a9840244a47efd4a0ca22e9628b88

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends python3=3.11.2-1+b1 \
    asciinema=2.2.0-1 \
    ca-certificates=20230311+deb12u1 \
    coreutils=9.1-1 \
    curl=7.88.1-10+deb12u14 \
    tmux=3.3a-3 \
    patch=2.7.6-7 \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/0.9.5/install.sh | sh \
    && . /root/.local/bin/env \
    && uv venv /opt/verifier-venv --python 3.11 \
    && uv pip install --python=/opt/verifier-venv/bin/python \
       pytest==8.4.1 pytest-json-ctrf==0.3.5 pytest-randomly==3.16.0

ENV PATH="/opt/verifier-venv/bin:/root/.local/bin:${PATH}"

COPY Cargo.toml Cargo.lock /app/
COPY p7 /app/p7
COPY m2 /app/m2
COPY data /app/data
COPY docs /app/docs

RUN cargo build --release --locked \
    && mkdir -p /app/bin /app/output /app/var/journal \
    && cp /app/target/release/journal_run /app/bin/journal_run

ENV PATH=/app/bin:${PATH}
