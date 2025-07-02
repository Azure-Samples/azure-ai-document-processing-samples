#!/usr/bin/env bash

###############################################################################
# Usage:
#   ./deploy.sh <deploymentName> <resourceGroupName> <location> [--what-if]
################################################################################

set -eu

# Setup STDERR.
err() {
    echo "(!) $*" >&2
}

# Validate arguments
if [ "$#" -lt 3 ]; then
    echo "Usage: $0 <deploymentName> <resourceGroupName> <location> [--what-if]" >&2
    exit 1
fi

DEPLOYMENT_NAME="$1"
RESOURCE_GROUP_NAME="$2"
LOCATION="$3"
WHAT_IF=false

# Check for --what-if in arguments
if [ "$#" -eq 3 ] && [ "$3" = "--what-if" ]; then
    WHAT_IF=true
fi

echo "Starting infrastructure deployment..."

# Ensure the working directory is the script's location
cd "$(dirname "$0")"

# Get the Azure AD principal ID of the authenticated user for the deployment
PRINCIPAL_ID=$(az ad signed-in-user show --query id -o tsv)
IDENTITY_ARRAY=$(jq -c -n --arg pid "$PRINCIPAL_ID" '[ { "principalId": $pid, "principalType": "User" } ]')

# Ensure the resource group exists
if [ "$(az group exists --name "$RESOURCE_GROUP_NAME")" != "true" ]; then
    echo "Resource group '$RESOURCE_GROUP_NAME' does not exist. Creating it..." >&2
    az group create --name "$RESOURCE_GROUP_NAME" --location "$LOCATION" || {
        err "Failed to create resource group '$RESOURCE_GROUP_NAME'."
        exit 1
    }
    echo "Resource group '$RESOURCE_GROUP_NAME' created successfully." >&2
else
    echo "Deploying to existing resource group '$RESOURCE_GROUP_NAME'." >&2
fi

# If --what-if is specified, preview the deployment
if [ "$WHAT_IF" = true ]; then
    echo "Previewing infrastructure deployment. No changes will be made." >&2

    set +e
    WHAT_IF_RESULT=$(az deployment group what-if \
        --name "$DEPLOYMENT_NAME" \
        --resource-group "$RESOURCE_GROUP_NAME" \
        --template-file '../bicep/main.bicep' \
        --parameters '../bicep/main.bicepparam' \
        --parameters workloadName="$DEPLOYMENT_NAME" \
        --parameters location="$LOCATION" \
        --parameters identities="$IDENTITY_ARRAY" \
        --no-pretty-print 2>/dev/null)
    EXIT_CODE=$?
    set -e

    if [ $EXIT_CODE -ne 0 ] || [ -z "$WHAT_IF_RESULT" ]; then
        echo "Infrastructure deployment preview failed." >&2
        exit 1
    fi

    echo "Infrastructure deployment preview succeeded." >&2

    echo "$WHAT_IF_RESULT" | jq '.changes'
    exit 0
fi

# Deploy the infrastructure
DEPLOYMENT_OUTPUTS=$(az deployment group create \
    --name "$DEPLOYMENT_NAME" \
    --resource-group "$RESOURCE_GROUP_NAME" \
    --template-file '../bicep/main.bicep' \
    --parameters '../bicep/main.bicepparam' \
    --parameters workloadName="$DEPLOYMENT_NAME" \
    --parameters location="$LOCATION" \
    --parameters identities="$IDENTITY_ARRAY" \
    --query properties.outputs -o json)

# If the deployment outputs are empty, we consider this an error
if [ -z "$DEPLOYMENT_OUTPUTS" ]; then
    echo "Infrastructure deployment failed." >&2
    exit 1
fi

echo "Updating .env file with deployment outputs..." >&2

ENV_PATH="../../.env"

if [ ! -f "$ENV_PATH" ]; then
    touch "$ENV_PATH"
fi

AZURE_RESOURCE_GROUP=$(echo "$DEPLOYMENT_OUTPUTS" | jq -r '.environmentInfo.value.azureResourceGroup')
AZURE_STORAGE_ACCOUNT_NAME=$(echo "$DEPLOYMENT_OUTPUTS" | jq -r '.environmentInfo.value.azureStorageAccountName')
AZURE_KEY_VAULT_NAME=$(echo "$DEPLOYMENT_OUTPUTS" | jq -r '.environmentInfo.value.azureKeyVaultName')
AZURE_AI_SERVICES_ENDPOINT=$(echo "$DEPLOYMENT_OUTPUTS" | jq -r '.environmentInfo.value.azureAIServicesEndpoint')
AZURE_OPENAI_ENDPOINT=$(echo "$DEPLOYMENT_OUTPUTS" | jq -r '.environmentInfo.value.azureOpenAIEndpoint')
AZURE_OPENAI_CHAT_DEPLOYMENT=$(echo "$DEPLOYMENT_OUTPUTS" | jq -r '.environmentInfo.value.azureOpenAIChatDeployment')
AZURE_OPENAI_TEXT_EMBEDDING_DEPLOYMENT=$(echo "$DEPLOYMENT_OUTPUTS" | jq -r '.environmentInfo.value.azureOpenAITextEmbeddingDeployment')
AZURE_AI_PHI_ENDPOINT=$(echo "$DEPLOYMENT_OUTPUTS" | jq -r '.environmentInfo.value.azureAIPhiEndpoint')
AZURE_AI_PHI_PRIMARY_KEY_SECRET_NAME=$(echo "$DEPLOYMENT_OUTPUTS" | jq -r '.environmentInfo.value.azureAIPhiPrimaryKeySecretName')
AZURE_AI_PHI_PRIMARY_KEY=$(az keyvault secret show \
    --name "$AZURE_AI_PHI_PRIMARY_KEY_SECRET_NAME" \
    --vault-name "$AZURE_KEY_VAULT_NAME" \
    --query value -o tsv)

echo "AZURE_RESOURCE_GROUP=$AZURE_RESOURCE_GROUP" >"$ENV_PATH"
echo "AZURE_STORAGE_ACCOUNT_NAME=$AZURE_STORAGE_ACCOUNT_NAME" >>"$ENV_PATH"
echo "AZURE_AI_SERVICES_ENDPOINT=$AZURE_AI_SERVICES_ENDPOINT" >>"$ENV_PATH"
echo "AZURE_OPENAI_ENDPOINT=$AZURE_OPENAI_ENDPOINT" >>"$ENV_PATH"
echo "AZURE_OPENAI_CHAT_DEPLOYMENT=$AZURE_OPENAI_CHAT_DEPLOYMENT" >>"$ENV_PATH"
echo "AZURE_OPENAI_TEXT_EMBEDDING_DEPLOYMENT=$AZURE_OPENAI_TEXT_EMBEDDING_DEPLOYMENT" >>"$ENV_PATH"
echo "AZURE_OPENAI_API_VERSION=2025-03-01-preview" >>"$ENV_PATH"
echo "AZURE_AI_PHI_ENDPOINT=$AZURE_AI_PHI_ENDPOINT" >>"$ENV_PATH"
echo "AZURE_AI_PHI_PRIMARY_KEY=$AZURE_AI_PHI_PRIMARY_KEY" >>"$ENV_PATH"

echo "Infrastructure deployment succeeded." >&2
exit 0
