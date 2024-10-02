@description('Name of the resource.')
param name string
@description('Location to deploy the resource. Defaults to the location of the resource group.')
param location string = resourceGroup().location
@description('Tags for the resource.')
param tags object = {}

@export()
@description('Key Vault configuration information for storing keys for serverless endpoint deployments.')
type keyVaultConfigInfo = {
  @description('Name of the key vault.')
  name: string
  @description('Name of the key for the primary key.')
  primaryKeySecretName: string
  @description('Name of the key for the secondary key.')
  secondaryKeySecretName: string
}

@export()
@description('Serverless model information for serverless endpoint deployments.')
type serverlessModelInfo = {
  @description('Name of the model. The model ID will be determined by the template.')
  name: string?
  @description('Model ID. Optional override if the expected model name is not supported. Value may start with azureml://.')
  id: string?
}

@export()
@description('Serverless model deployment information.')
type serverlessModelDeploymentInfo = {
  @description('Name for the serverless model deployment.')
  name: string
  @description('Serverless model information.')
  model: serverlessModelInfo
  @description('Key Vault configuration for the serverless model deployment.')
  keyVaultConfig: keyVaultConfigInfo
}

@export()
@description('Output information for serverless endpoint deployments.')
type serverlessModelDeploymentOutputInfo = {
  @description('ID for the deployed AI model serverless endpoint resource.')
  id: string
  @description('Name for the deployed AI model serverless endpoint resource.')
  name: string
  @description('Inference endpoint for the deployed AI model serverless endpoint resource.')
  endpoint: string
  @description('Primary key secret name for the deployed AI model serverless endpoint resource.')
  primaryKeySecretName: string
  @description('Secondary key secret name for the deployed AI model serverless endpoint resource.')
  secondaryKeySecretName: string
}

@description('Name for the AI Hub resource to deploy the serverless endpoint to.')
param aiHubName string
@description('Model to deploy as a serverless endpoint.')
param model serverlessModelInfo
@description('Key Vault configuration to store endpoint keys.')
param keyVaultConfig keyVaultConfigInfo?

var models = loadJsonContent('./models.json')
var modelId = contains(model, 'id') ? model.id! : models.serverless[model.name!]

resource aiHub 'Microsoft.MachineLearningServices/workspaces@2024-07-01-preview' existing = {
  name: aiHubName
}

resource modelServerlessEndpoint 'Microsoft.MachineLearningServices/workspaces/serverlessEndpoints@2024-07-01-preview' = {
  name: name
  location: location
  tags: tags
  parent: aiHub
  sku: {
    name: 'Consumption'
  }
  properties: {
    modelSettings: {
      modelId: modelId
    }
    authMode: 'Key'
  }
}

module primaryKeySecret '../security/key-vault-secret.bicep' = if (keyVaultConfig != null) {
  name: keyVaultConfig!.primaryKeySecretName
  params: {
    name: keyVaultConfig!.primaryKeySecretName
    keyVaultName: keyVaultConfig!.name
    value: modelServerlessEndpoint.listKeys().primaryKey
  }
}

module secondaryKeySecret '../security/key-vault-secret.bicep' = if (keyVaultConfig != null) {
  name: keyVaultConfig!.secondaryKeySecretName
  params: {
    name: keyVaultConfig!.secondaryKeySecretName
    keyVaultName: keyVaultConfig!.name
    value: modelServerlessEndpoint.listKeys().secondaryKey
  }
}

@description('ID for the deployed AI model serverless endpoint resource.')
output id string = modelServerlessEndpoint.id
@description('Name for the deployed AI model serverless endpoint resource.')
output name string = modelServerlessEndpoint.name
@description('Inference endpoint for the deployed AI model serverless endpoint resource.')
output endpoint string = modelServerlessEndpoint.properties.inferenceEndpoint.uri
@description('Primary key secret name for the deployed AI model serverless endpoint resource.')
output primaryKeySecretName string = keyVaultConfig != null ? keyVaultConfig!.primaryKeySecretName : ''
@description('Secondary key secret name for the deployed AI model serverless endpoint resource.')
output secondaryKeySecretName string = keyVaultConfig != null ? keyVaultConfig!.secondaryKeySecretName : ''
