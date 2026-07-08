FROM python:3.13-slim-bookworm@sha256:f576b530293e74140ea91d262232648d5c4f45640a95ec447757701bfcacf034

# terminus-2 agent harness requires tmux + asciinema in the image (not at verifier runtime).
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        asciinema=2.2.0-1 \
        build-essential=12.9 \
        ca-certificates=20230311+deb12u1 \
        cmake=3.25.1-1 \
        curl=7.88.1-10+deb12u14 \
        g++=4:12.2.0-3 \
        make=4.3-4.1 \
        tmux=3.3a-3 \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /app/bin /app/output

RUN python -m pip install --no-cache-dir \
    pytest==8.4.1 \
    pytest-json-ctrf==0.3.5 \
    pytest-randomly==3.16.0

WORKDIR /app

COPY . /app/environment

ENV PATH="/app/bin:$PATH"
