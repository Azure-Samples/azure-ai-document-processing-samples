<#
.SYNOPSIS
    Deploys the infrastructure and applications required to run the solution.
.PARAMETER DeploymentName
	The name of the deployment.
.PARAMETER Location
    The location of the deployment.
.PARAMETER SkipInfrastructure
    Whether to skip the infrastructure deployment. Requires InfrastructureOutputs.json to exist in the infra directory.
.EXAMPLE
    .\Setup-Environment.ps1 -DeploymentName 'ai-document-data-extraction' -Location 'eastus' -SkipInfrastructure $false
.NOTES
    Author: James Croft
#>

param
(
    [Parameter(Mandatory = $true)]
    [string]$DeploymentName,
    [Parameter(Mandatory = $true)]
    [string]$Location,
    [Parameter(Mandatory = $true)]
    [string]$SkipInfrastructure
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

if ($SkipInfrastructure -eq '$false' -or -not (Test-Path -Path './infra/InfrastructureOutputs.json')) {
    Write-Host "Deploying infrastructure..."
    $InfrastructureOutputs = (./infra/Deploy-Infrastructure.ps1 `
            -DeploymentName $DeploymentName `
            -Location $Location)
}
else {
    Write-Host "Skipping infrastructure deployment. Using existing outputs..."
    $InfrastructureOutputs = Get-Content -Path './infra/InfrastructureOutputs.json' -Raw | ConvertFrom-Json
}

if (-not $InfrastructureOutputs) {
    Write-Error "Infrastructure deployment outputs are not available. Exiting..."
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
$Phi35MiniEndpoint = $InfrastructureOutputs.aiModelsInfo.value.phi35MiniEndpoint

$Phi35MiniPrimaryKeySecretName = $InfrastructureOutputs.aiModelsInfo.value.phi35MiniPrimaryKeySecretName
$Phi35MiniPrimaryKey = (az keyvault secret show --vault-name $KeyVaultName --name $Phi35MiniPrimaryKeySecretName --query value -o tsv)

Write-Host "Updating local settings..."

$ConfigurationFile = './.env'

Set-ConfigurationFileVariable -configurationFile $ConfigurationFile -variableName 'RESOURCE_GROUP_NAME' -variableValue $ResourceGroupName
Set-ConfigurationFileVariable -configurationFile $ConfigurationFile -variableName 'MANAGED_IDENTITY_CLIENT_ID' -variableValue $ManagedIdentityClientId
Set-ConfigurationFileVariable -configurationFile $ConfigurationFile -variableName 'STORAGE_ACCOUNT_NAME' -variableValue $StorageAccountName
Set-ConfigurationFileVariable -configurationFile $ConfigurationFile -variableName 'AI_SERVICES_ENDPOINT' -variableValue $AIServicesEndpoint
Set-ConfigurationFileVariable -configurationFile $ConfigurationFile -variableName 'OPENAI_ENDPOINT' -variableValue $OpenAIEndpoint
Set-ConfigurationFileVariable -configurationFile $ConfigurationFile -variableName 'GPT4O_MODEL_DEPLOYMENT_NAME' -variableValue $Gpt4oModelDeploymentName
Set-ConfigurationFileVariable -configurationFile $ConfigurationFile -variableName 'TEXT_EMBEDDING_MODEL_DEPLOYMENT_NAME' -variableValue $TextEmbeddingModelDeploymentName
Set-ConfigurationFileVariable -configurationFile $ConfigurationFile -variableName 'PHI35_MINI_ENDPOINT' -variableValue $Phi35MiniEndpoint
Set-ConfigurationFileVariable -configurationFile $ConfigurationFile -variableName 'PHI35_MINI_PRIMARY_KEY' -variableValue $Phi35MiniPrimaryKey