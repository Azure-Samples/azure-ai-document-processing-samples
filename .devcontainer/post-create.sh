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

# Install the local dependencies for dotnet
dotnet restore requirements.csproj
dotnet store --manifest requirements.csproj --framework net8.0 --runtime linux-x64 --skip-optimization --output /workspaces/azure-ai-document-processing-samples/share/dotnet/store
export DOTNET_SHARED_STORE=/workspaces/azure-ai-document-processing-samples/share/dotnet/store