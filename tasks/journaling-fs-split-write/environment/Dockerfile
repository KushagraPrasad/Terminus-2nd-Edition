FROM public.ecr.aws/docker/library/python:3.13-slim-bookworm@sha256:01f42367a0a94ad4bc17111776fd66e3500c1d87c15bbd6055b7371d39c124fb

WORKDIR /app

# Install system tools and build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends tmux=3.3a-3 asciinema=2.2.0-1 build-essential=12.9 ca-certificates=20230311+deb12u1 gcc=4:12.2.0-3 make=4.3-4.1 && rm -rf /var/lib/apt/lists/*

# Install pytest using system Python (no venv needed)
RUN python -m pip install --no-cache-dir pytest==8.4.1 pytest-json-ctrf==0.3.5

# Create required directories
RUN mkdir -p /app/environment /data /app/output /app/build

# Copy task files
COPY . /app/environment

# Set environment
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV PYTHONPATH=/app

WORKDIR /app/environment
RUN make
