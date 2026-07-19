#!/bin/bash
set -e

# ROOT_DIR is set by collapse_check to the host folder.
# In container execution, if ROOT_DIR is not set, we default to /app/solution.
ROOT_DIR=${ROOT_DIR:-/app/solution}
if [ ! -f "$ROOT_DIR/solution.patch" ]; then
    if [ -f "/solution/solution.patch" ]; then
        ROOT_DIR="/solution"
    elif [ -f "./solution/solution.patch" ]; then
        ROOT_DIR="./solution"
    fi
fi

patch -p1 < "$ROOT_DIR/solution.patch"

make
