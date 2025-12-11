#!/bin/bash
set -e

# Directory to save the compiled binaries
BIN_DIR="./python/teams_lib_pzsp2_z1/bin"
mkdir -p "$BIN_DIR"

# Path to Go bridge
BRIDGE_PATH="./go/bridge/"

# Read the mode from the first argument
MODE=$1

if [[ "$MODE" == "real" ]]; then
    echo "=== Building REAL mode (Production) ==="

    echo "Building Linux (real)..."
    GOOS=linux GOARCH=amd64 go build -tags real -o "$BIN_DIR/teamsClientLib_linux" "$BRIDGE_PATH"

    echo "Building Windows (real)..."
    GOOS=windows GOARCH=amd64 go build -tags real -o "$BIN_DIR/teamsClientLib_windows.exe" "$BRIDGE_PATH"

elif [[ "$MODE" == "fake" ]]; then
    echo "=== Building FAKE mode (Integration Tests) ==="

    echo "Building Linux (fake)..."
    GOOS=linux GOARCH=amd64 go build -tags fake -o "$BIN_DIR/teamsClientLib_linux" "$BRIDGE_PATH"

else
    echo "Error: Invalid argument. Usage: $0 [real|fake]"
    echo "  real - builds for Linux and Windows with production code"
    echo "  fake - builds for Linux only with mock capability"
    exit 1
fi

echo "Done! Binaries saved in $BIN_DIR"