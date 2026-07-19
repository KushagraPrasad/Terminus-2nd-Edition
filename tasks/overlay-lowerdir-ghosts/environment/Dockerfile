FROM rust:1.84-bookworm@sha256:738ae99a3d75623f41e6882566b4ef37e38a9840244a47efd4a0ca22e9628b88 AS builder

WORKDIR /build
ENV CARGO_TARGET_DIR=/build/target

COPY Cargo.toml Cargo.lock /build/
COPY p7 /build/p7
COPY m2 /build/m2
COPY data /build/data
COPY docs /build/docs

RUN cd /build && cargo build --release --locked

FROM python:3.13-slim-bookworm@sha256:e4fa1f978c539608a10cdf74700ac32a3f719dfc6e8b6b6001da82deb36302a2

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    asciinema=2.2.0-1 \
    build-essential=12.9 \
    ca-certificates=20230311+deb12u1 \
    coreutils=9.1-1 \
    patch=2.7.6-7 \
    tmux=3.3a-3 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    pytest==8.4.1 \
    pytest-json-ctrf==0.3.5 \
    pytest-randomly==3.16.0

COPY --from=builder /usr/local/cargo /usr/local/cargo
COPY --from=builder /usr/local/rustup /usr/local/rustup

ENV RUSTUP_HOME=/usr/local/rustup \
    CARGO_HOME=/usr/local/cargo \
    PATH="/usr/local/cargo/bin:${PATH}" \
    CARGO_TARGET_DIR=/app/target

COPY --from=builder /build/Cargo.toml /build/Cargo.lock /app/
COPY --from=builder /build/p7 /app/p7
COPY --from=builder /build/m2 /app/m2
COPY --from=builder /build/data /app/data
COPY --from=builder /build/docs /app/docs
COPY --from=builder /build/target /app/target

RUN mkdir -p /app/bin \
    && cp /app/target/release/atlasd /app/bin/atlasd

ENV PATH="/app/bin:/usr/local/cargo/bin:${PATH}"
