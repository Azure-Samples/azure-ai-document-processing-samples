param
(
    [Parameter(Mandatory = $true)]
    [string]$DeploymentName,
    [Parameter(Mandatory = $true)]
    [string]$Location,
    [switch]$WhatIf
)

function Set-ConfigurationFileVariable($configurationFile, $variableName, $variableValue) {
    if (Select-String -Path $configurationFile -Pattern $variableName) {
        (Get-Content $configurationFile) | Foreach-Object {
            $_ -replace "$variableName = .*", "$variableName = $variableValue"
        } | Set-Content $configurationFile
    }
    else {
        Add-Content -Path $configurationFile -value "$variableName = $variableValue"
    }
}

Write-Host "Starting environment setup..."

Write-Host "Deploying infrastructure..."
$InfrastructureOutputs = (./infra/Deploy-Infrastructure.ps1 `
        -DeploymentName $DeploymentName `
        -Location $Location `
        -WhatIf:$WhatIf)

if (-not $InfrastructureOutputs) {
    Write-Error "Failed to deploy infrastructure."
    exit 1
}

$ResourceGroupName = $InfrastructureOutputs.resourceGroupInfo.value.name
$ManagedIdentityClientId = $InfrastructureOutputs.managedIdentityInfo.value.clientId
$StorageAccountName = $InfrastructureOutputs.storageAccountInfo.value.name
$KeyVaultName = $InfrastructureOutputs.keyVaultInfo.value.name
$AIServicesEndpoint = $InfrastructureOutputs.aiModelsInfo.value.aiServicesEndpoint
$OpenAIEndpoint = $InfrastructureOutputs.aiModelsInfo.value.openAIEndpoint
$Gpt4oModelDeploymentName = $InfrastructureOutputs.aiModelsInfo.value.gpt4oModelDeploymentName
$TextEmbeddingModelDeploymentName = $InfrastructureOutputs.aiModelsInfo.value.textEmbeddingModelDeploymentName
$Phi3Endpoint = $InfrastructureOutputs.aiModelsInfo.value.phi3Endpoint

$Phi3PrimaryKeySecretName = $InfrastructureOutputs.aiModelsInfo.value.phi3PrimaryKeySecretName
$Phi3PrimaryKey = (az keyvault secret show --vault-name $KeyVaultName --name $Phi3PrimaryKeySecretName --query value -o tsv)

Write-Host "Updating local settings..."

$ConfigurationFile = './.env'
if (-not (Test-Path -Path $ConfigurationFile)) {
    New-Item -Path $ConfigurationFile -ItemType File
}

Set-ConfigurationFileVariable -configurationFile $ConfigurationFile -variableName 'RESOURCE_GROUP_NAME' -variableValue $ResourceGroupName
Set-ConfigurationFileVariable -configurationFile $ConfigurationFile -variableName 'MANAGED_IDENTITY_CLIENT_ID' -variableValue $ManagedIdentityClientId
Set-ConfigurationFileVariable -configurationFile $ConfigurationFile -variableName 'STORAGE_ACCOUNT_NAME' -variableValue $StorageAccountName
Set-ConfigurationFileVariable -configurationFile $ConfigurationFile -variableName 'AI_SERVICES_ENDPOINT' -variableValue $AIServicesEndpoint
Set-ConfigurationFileVariable -configurationFile $ConfigurationFile -variableName 'OPENAI_ENDPOINT' -variableValue $OpenAIEndpoint
Set-ConfigurationFileVariable -configurationFile $ConfigurationFile -variableName 'GPT4O_MODEL_DEPLOYMENT_NAME' -variableValue $Gpt4oModelDeploymentName
Set-ConfigurationFileVariable -configurationFile $ConfigurationFile -variableName 'TEXT_EMBEDDING_MODEL_DEPLOYMENT_NAME' -variableValue $TextEmbeddingModelDeploymentName
Set-ConfigurationFileVariable -configurationFile $ConfigurationFile -variableName 'PHI3_ENDPOINT' -variableValue $Phi3Endpoint
Set-ConfigurationFileVariable -configurationFile $ConfigurationFile -variableName 'PHI3_PRIMARY_KEY' -variableValue $Phi3PrimaryKey