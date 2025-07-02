#!/usr/bin/env bash

USERNAME=${USERNAME:-"vscode"}

set -eux

# Setup STDERR.
err() {
    echo "(!) $*" >&2
}

# Ensure apt is in non-interactive to avoid prompts
export DEBIAN_FRONTEND=noninteractive

# Find all requirements.txt files in the repo directory and install them
find ./ -name "requirements.txt" | while read -r requirements; do
    echo "Installing requirements from $requirements"
    pip install -r "$requirements"
done
