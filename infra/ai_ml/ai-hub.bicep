import { roleAssignmentInfo } from '../security/managed-identity.bicep'
import { serverlessModelDeploymentInfo, serverlessModelDeploymentOutputInfo } from './ai-hub-model-serverless-endpoint.bicep'
import { connectionInfo } from 'ai-hub-connection.bicep'

@description('Name of the resource.')
param name string
@description('Location to deploy the resource. Defaults to the location of the resource group.')
param location string = resourceGroup().location
@description('Tags for the resource.')
param tags object = {}

@description('Friendly name for the AI Hub.')
param friendlyName string = name
@description('Description for the AI Hub.')
param descriptionInfo string = 'Azure AI Hub'
@description('Isolation mode for the AI Hub.')
@allowed([
  'AllowInternetOutbound'
  'AllowOnlyApprovedOutbound'
  'Disabled'
])
param isolationMode string = 'Disabled'
@description('Whether to enable public network access. Defaults to Enabled.')
@allowed([
  'Enabled'
  'Disabled'
])
param publicNetworkAccess string = 'Enabled'
@description('Whether or not to use credentials for the system datastores of the workspace. Defaults to identity.')
@allowed([
  'accessKey'
  'identity'
])
param systemDatastoresAuthMode string = 'identity'
@description('ID for the Storage Account associated with the AI Hub.')
param storageAccountId string
@description('ID for the Key Vault associated with the AI Hub.')
param keyVaultId string
@description('ID for the Application Insights associated with the AI Hub.')
param applicationInsightsId string
@description('ID for the Container Registry associated with the AI Hub.')
param containerRegistryId string
@description('ID for the Managed Identity associated with the AI Hub. Defaults to the system-assigned identity.')
param identityId string?
@description('Name for the AI Services resource to connect to.')
param aiServicesName string
@description('Serverless model deployments for the AI Hub.')
param serverlessModels serverlessModelDeploymentInfo[] = []
@description('Resource connections associated with the AI Hub.')
param connections connectionInfo[] = []
@description('Role assignments to create for the AI Hub instance.')
param roleAssignments roleAssignmentInfo[] = []

resource aiServices 'Microsoft.CognitiveServices/accounts@2024-04-01-preview' existing = {
  name: aiServicesName
}

resource aiHub 'Microsoft.MachineLearningServices/workspaces@2024-04-01-preview' = {
  name: name
  location: location
  tags: tags
  kind: 'Hub'
  identity: {
    type: identityId == null ? 'SystemAssigned' : 'UserAssigned'
    userAssignedIdentities: identityId == null
      ? null
      : {
          '${identityId}': {}
        }
  }
  sku: {
    name: 'Basic'
    tier: 'Basic'
  }
  properties: {
    friendlyName: friendlyName
    description: descriptionInfo
    managedNetwork: {
      isolationMode: isolationMode
    }
    publicNetworkAccess: publicNetworkAccess
    storageAccount: storageAccountId
    keyVault: keyVaultId
    applicationInsights: applicationInsightsId
    containerRegistry: containerRegistryId
    systemDatastoresAuthMode: systemDatastoresAuthMode
    primaryUserAssignedIdentity: identityId
  }

  resource aiServicesConnection 'connections@2024-04-01-preview' = {
    name: '${aiServicesName}-connection'
    properties: {
      category: 'AIServices'
      target: aiServices.properties.endpoint
      authType: 'AAD'
      isSharedToAll: true
      metadata: {
        ApiType: 'Azure'
        ResourceId: aiServices.id
      }
    }
  }
}

module aiHubConnections 'ai-hub-connection.bicep' = [
  for connection in connections: {
    name: connection.name
    params: {
      aiHubName: aiHub.name
      connection: connection
    }
  }
]

module serverlessModelEndpoints 'ai-hub-model-serverless-endpoint.bicep' = [
  for serverlessModel in serverlessModels: {
    name: serverlessModel.name
    params: {
      name: serverlessModel.name
      aiHubName: aiHub.name
      model: serverlessModel.model
      keyVaultConfig: serverlessModel.keyVaultConfig
    }
  }
]

resource assignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = [
  for roleAssignment in roleAssignments: {
    name: guid(aiHub.id, roleAssignment.principalId, roleAssignment.roleDefinitionId)
    scope: aiHub
    properties: {
      principalId: roleAssignment.principalId
      roleDefinitionId: roleAssignment.roleDefinitionId
      principalType: roleAssignment.principalType
    }
  }
]

@description('ID for the deployed AI Hub resource.')
output id string = aiHub.id
@description('Name for the deployed AI Hub resource.')
output name string = aiHub.name
@description('Identity principal ID for the deployed AI Hub resource.')
output identityPrincipalId string? = identityId == null ? aiHub.identity.principalId : identityId
@description('Serverless model deployments for the AI Hub.')
output serverlessModelDeployments serverlessModelDeploymentOutputInfo[] = [
  for (item, index) in serverlessModels: {
    id: serverlessModelEndpoints[index].outputs.id
    name: serverlessModelEndpoints[index].outputs.name
    endpoint: serverlessModelEndpoints[index].outputs.endpoint
    primaryKeySecretName: serverlessModelEndpoints[index].outputs.primaryKeySecretName
    secondaryKeySecretName: serverlessModelEndpoints[index].outputs.secondaryKeySecretName
  }
]
