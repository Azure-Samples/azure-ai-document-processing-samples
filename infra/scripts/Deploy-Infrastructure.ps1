param
(
    [Parameter(Mandatory = $true)]
    [string]$DeploymentName,
    [Parameter(Mandatory = $true)]
    [string]$ResourceGroupName,
    [Parameter(Mandatory = $true)]
    [string]$Location,
    [switch]$WhatIf
)

function Set-EnvVariable($envPath, $variableName, $variableValue) {
    if (Select-String -Path $envPath -Pattern $variableName) {
        (Get-Content $envPath) | Foreach-Object {
            $_ -replace "$variableName=.*", "$variableName=$variableValue"
        } | Set-Content $envPath
    }
    else {
        Add-Content -Path $envPath -Value "$variableName=$variableValue"
    }
}

Write-Host "Starting infrastructure deployment..."

# Ensure the working directory is the script's location
Push-Location -Path $PSScriptRoot

# Get the Azure AD principal ID of the authenticated user for the deployment
$principalId = (az ad signed-in-user show --query id -o tsv)
$identity = @{
    "principalId"   = "$principalId"
    "principalType" = "User"
}
$identityArray = ConvertTo-Json @($identity) -Depth 5 -Compress

# Ensure the resource group exists
if (-not (az group exists --name $ResourceGroupName)) {
    Write-Host "Resource group '$ResourceGroupName' does not exist. Creating it..."
    az group create --name $ResourceGroupName --location $Location | Out-Null
}
else {
    Write-Host "Deploying to existing resource group '$ResourceGroupName'."
}

# If -WhatIf is specified, preview the deployment
if ($whatIf) {
    Write-Host "Previewing Azure infrastructure deployment. No changes will be made."

    $result = (az deployment group what-if `
            --name $DeploymentName `
            --resource-group $ResourceGroupName `
            --template-file '../bicep/main.bicep' `
            --parameters '../bicep/main.bicepparam' `
            --parameters workloadName=$DeploymentName `
            --parameters location=$Location `
            --parameters identities=$identityArray `
            --no-pretty-print) | ConvertFrom-Json

    if (-not $result) {
        Write-Error "Infrastructure deployment preview failed."
        exit 1
    }

    Write-Host "Infrastructure deployment preview succeeded."
    $result.changes | Format-List
    exit
}

$deploymentOutputs = (az deployment group create `
        --name $DeploymentName `
        --resource-group $ResourceGroupName `
        --template-file '../bicep/main.bicep' `
        --parameters '../bicep/main.bicepparam' `
        --parameters workloadName=$DeploymentName `
        --parameters location=$Location `
        --parameters identities=$identityArray `
        --query properties.outputs -o json) | ConvertFrom-Json

if (-not $deploymentOutputs) {
    Write-Error "Infrastructure deployment failed."
    exit 1
}

Write-Host "Updating .env file with deployment outputs..."

$envPath = "../../.env"

if (-not (Test-Path -Path $envPath)) {
    New-Item -Path $envPath -ItemType File
}

$azureResourceGroup = $deploymentOutputs.environmentInfo.value.azureResourceGroup
$azureStorageAccountName = $deploymentOutputs.environmentInfo.value.azureStorageAccountName
$azureKeyVaultName = $deploymentOutputs.environmentInfo.value.azureKeyVaultName
$azureAIServicesEndpoint = $deploymentOutputs.environmentInfo.value.azureAIServicesEndpoint
$azureOpenAIEndpoint = $deploymentOutputs.environmentInfo.value.azureOpenAIEndpoint
$azureOpenAIChatDeployment = $deploymentOutputs.environmentInfo.value.azureOpenAIChatDeployment
$azureOpenAITextEmbeddingDeployment = $deploymentOutputs.environmentInfo.value.azureOpenAITextEmbeddingDeployment
$azureAIPhiEndpoint = $deploymentOutputs.environmentInfo.value.azureAIPhiEndpoint
$azureAIPhiPrimaryKeySecretName = $deploymentOutputs.environmentInfo.value.azureAIPhiPrimaryKeySecretName
$azureAIPhiPrimaryKey = (az keyvault secret show --vault-name $azureKeyVaultName --name $azureAIPhiPrimaryKeySecretName --query value -o tsv)

Set-EnvVariable -envPath $envPath -variableName 'AZURE_RESOURCE_GROUP' -variableValue $azureResourceGroup
Set-EnvVariable -envPath $envPath -variableName 'AZURE_STORAGE_ACCOUNT_NAME' -variableValue $azureStorageAccountName
Set-EnvVariable -envPath $envPath -variableName 'AZURE_AI_SERVICES_ENDPOINT' -variableValue $azureAIServicesEndpoint
Set-EnvVariable -envPath $envPath -variableName 'AZURE_OPENAI_ENDPOINT' -variableValue $azureOpenAIEndpoint
Set-EnvVariable -envPath $envPath -variableName 'AZURE_OPENAI_CHAT_DEPLOYMENT' -variableValue $azureOpenAIChatDeployment
Set-EnvVariable -envPath $envPath -variableName 'AZURE_OPENAI_TEXT_EMBEDDING_DEPLOYMENT' -variableValue $azureOpenAITextEmbeddingDeployment
Set-EnvVariable -envPath $envPath -variableName 'AZURE_OPENAI_API_VERSION' -variableValue '2025-03-01-preview'
Set-EnvVariable -envPath $envPath -variableName 'AZURE_AI_PHI_ENDPOINT' -variableValue $azureAIPhiEndpoint
Set-EnvVariable -envPath $envPath -variableName 'AZURE_AI_PHI_PRIMARY_KEY' -variableValue $azureAIPhiPrimaryKey

Write-Host "Infrastructure deployment succeeded."

Pop-Location

return $deploymentOutputs
