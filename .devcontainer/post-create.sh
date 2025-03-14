#!/usr/bin/env bash

USERNAME=${USERNAME:-"vscode"}

set -eux

# Setup STDERR.
err() {
    echo "(!) $*" >&2
}

# Ensure apt is in non-interactive to avoid prompts
export DEBIAN_FRONTEND=noninteractive

# Install the local dependencies for Python
pip --disable-pip-version-check --no-cache-dir install --user -r requirements.txt