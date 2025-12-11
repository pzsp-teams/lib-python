#!/bin/bash
set -e

# Directory to save the compiled binaries
BIN_DIR="./python/teams_lib_pzsp2_z1/bin"
mkdir -p "$BIN_DIR"

# Path to Go bridge
BRIDGE_PATH="./go/bridge/"

echo "Building Linux..."
GOOS=linux GOARCH=amd64 go build -o "$BIN_DIR/teamsClientLib_linux" "$BRIDGE_PATH"

echo "Building Windows..."
GOOS=windows GOARCH=amd64 go build -o "$BIN_DIR/teamsClientLib_windows.exe" "$BRIDGE_PATH"

echo "Done! Binaries saved in $BIN_DIR"