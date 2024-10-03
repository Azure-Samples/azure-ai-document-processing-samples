import { roleAssignmentInfo } from '../security/managed-identity.bicep'
import { serverlessModelDeploymentInfo, serverlessModelDeploymentOutputInfo } from './ai-hub-model-serverless-endpoint.bicep'
import { connectionInfo } from 'ai-hub-connection.bicep'

@description('Name of the resource.')
param name string
@description('Location to deploy the resource. Defaults to the location of the resource group.')
param location string = resourceGroup().location
@description('Tags for the resource.')
param tags object = {}

@description('Name for the AI Hub resource associated with the AI Hub project.')
param aiHubName string
@description('Friendly name for the AI Hub project.')
param friendlyName string = name
@description('Description for the AI Hub project.')
param descriptionInfo string = 'Azure AI Hub Project'
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
@description('ID for the Managed Identity associated with the AI Hub project. Defaults to the system-assigned identity.')
param identityId string?
@description('Serverless model deployments for the AI Hub project.')
param serverlessModels serverlessModelDeploymentInfo[] = []
@description('Resource connections associated with the AI Hub project.')
param connections connectionInfo[] = []
@description('Role assignments to create for the AI Hub project instance.')
param roleAssignments roleAssignmentInfo[] = []

resource aiHub 'Microsoft.MachineLearningServices/workspaces@2024-04-01-preview' existing = {
  name: aiHubName
}

resource aiHubProject 'Microsoft.MachineLearningServices/workspaces@2024-04-01-preview' = {
  name: name
  location: location
  tags: tags
  kind: 'Project'
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
    hubResourceId: aiHub.id
    publicNetworkAccess: publicNetworkAccess
    systemDatastoresAuthMode: systemDatastoresAuthMode
    primaryUserAssignedIdentity: identityId
  }
}

module aiHubConnections 'ai-hub-connection.bicep' = [
  for connection in connections: {
    name: connection.name
    params: {
      aiHubName: aiHubProject.name
      connection: connection
    }
  }
]

module serverlessModelEndpoints 'ai-hub-model-serverless-endpoint.bicep' = [
  for serverlessModel in serverlessModels: {
    name: serverlessModel.name
    params: {
      name: serverlessModel.name
      aiHubName: aiHubProject.name
      model: serverlessModel.model
      keyVaultConfig: serverlessModel.keyVaultConfig
    }
  }
]

resource assignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = [
  for roleAssignment in roleAssignments: {
    name: guid(aiHubProject.id, roleAssignment.principalId, roleAssignment.roleDefinitionId)
    scope: aiHubProject
    properties: {
      principalId: roleAssignment.principalId
      roleDefinitionId: roleAssignment.roleDefinitionId
      principalType: roleAssignment.principalType
    }
  }
]

@description('ID for the deployed AI Hub project resource.')
output id string = aiHubProject.id
@description('Name for the deployed AI Hub project resource.')
output name string = aiHubProject.name
@description('Identity principal ID for the deployed AI Hub project resource.')
output identityPrincipalId string? = identityId == null ? aiHubProject.identity.principalId : identityId
@description('Serverless model deployments for the AI Hub project.')
output serverlessModelDeployments serverlessModelDeploymentOutputInfo[] = [
  for (item, index) in serverlessModels: {
    id: serverlessModelEndpoints[index].outputs.id
    name: serverlessModelEndpoints[index].outputs.name
    endpoint: serverlessModelEndpoints[index].outputs.endpoint
    primaryKeySecretName: serverlessModelEndpoints[index].outputs.primaryKeySecretName
    secondaryKeySecretName: serverlessModelEndpoints[index].outputs.secondaryKeySecretName
  }
]
