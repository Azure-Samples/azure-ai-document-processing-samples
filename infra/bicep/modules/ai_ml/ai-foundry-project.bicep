import { roleAssignmentInfo } from '../security/managed-identity.bicep'
import { serverlessModelDeploymentInfo, serverlessModelDeploymentOutputInfo } from './ai-foundry-model-serverless-endpoint.bicep'
import { connectionInfo } from 'ai-foundry-hub-connection.bicep'
import { diagnosticSettingsInfo } from '../management_governance/log-analytics-workspace.bicep'

@description('Name of the resource.')
param name string
@description('Location to deploy the resource. Defaults to the location of the resource group.')
param location string = resourceGroup().location
@description('Tags for the resource.')
param tags object = {}

@description('Name for the AI Foundry Hub resource associated with the AI Foundry Project.')
param aiFoundryHubName string
@description('Friendly name for the AI Foundry Project.')
param friendlyName string = name
@description('Description for the AI Foundry Project.')
param descriptionInfo string = 'Azure AI Foundry Project'
@description('Whether to enable public network access. Defaults to Enabled.')
param publicNetworkAccess 'Enabled' | 'Disabled' | 'SecuredByPerimeter' = 'Enabled'
@description('Whether or not to use credentials for the system datastores of the workspace. Defaults to identity.')
@allowed([
  'accessKey'
  'identity'
])
param systemDatastoresAuthMode string = 'identity'
@description('ID for the Managed Identity associated with the AI Foundry Project. Defaults to the system-assigned identity.')
param identityId string?
@description('Serverless model deployments for the AI Foundry Project.')
param serverlessModels serverlessModelDeploymentInfo[] = []
@description('Resource connections associated with the AI Foundry Project.')
param connections connectionInfo[] = []
@description('Role assignments to create for the AI Foundry Project instance.')
param roleAssignments roleAssignmentInfo[] = []
@description('Name of the Log Analytics Workspace to use for diagnostic settings.')
param logAnalyticsWorkspaceName string?
@description('Diagnostic settings to configure for the AI Foundry Project instance. Defaults to all logs and metrics.')
param diagnosticSettings diagnosticSettingsInfo = {
  logs: [
    {
      categoryGroup: 'allLogs'
      enabled: true
    }
  ]
  metrics: [
    {
      category: 'AllMetrics'
      enabled: true
    }
  ]
}

// Deployments

resource aiFoundryHub 'Microsoft.MachineLearningServices/workspaces@2025-01-01-preview' existing = {
  name: aiFoundryHubName
}

resource aiFoundryProject 'Microsoft.MachineLearningServices/workspaces@2025-01-01-preview' = {
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
    hubResourceId: aiFoundryHub.id
    publicNetworkAccess: publicNetworkAccess
    systemDatastoresAuthMode: systemDatastoresAuthMode
    primaryUserAssignedIdentity: identityId
  }
}

module aiFoundryProjectConnections 'ai-foundry-hub-connection.bicep' = [
  for connection in connections: {
    name: connection.name
    params: {
      aiFoundryName: aiFoundryProject.name
      connection: connection
    }
  }
]

module serverlessModelEndpoints 'ai-foundry-model-serverless-endpoint.bicep' = [
  for serverlessModel in serverlessModels: {
    name: serverlessModel.name
    params: {
      name: serverlessModel.name
      location: location
      tags: union(tags, {})
      aiFoundryName: aiFoundryProject.name
      model: serverlessModel.model
      keyVaultConfig: serverlessModel.keyVaultConfig
    }
  }
]

resource assignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = [
  for roleAssignment in roleAssignments: {
    name: guid(aiFoundryProject.id, roleAssignment.principalId, roleAssignment.roleDefinitionId)
    scope: aiFoundryProject
    properties: {
      principalId: roleAssignment.principalId
      roleDefinitionId: roleAssignment.roleDefinitionId
      principalType: roleAssignment.principalType
    }
  }
]

resource logAnalyticsWorkspace 'Microsoft.OperationalInsights/workspaces@2025-02-01' existing = if (logAnalyticsWorkspaceName != null) {
  name: logAnalyticsWorkspaceName!
}

resource aiFoundryProjectDiagnosticSettings 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = if (logAnalyticsWorkspaceName != null) {
  name: '${aiFoundryProject.name}-diagnostic-settings'
  scope: aiFoundryProject
  properties: {
    workspaceId: logAnalyticsWorkspace.id
    logs: diagnosticSettings!.logs
    metrics: diagnosticSettings!.metrics
  }
}

// Outputs

@description('ID for the deployed AI Foundry Project resource.')
output id string = aiFoundryProject.id
@description('Name for the deployed AI Foundry Project resource.')
output name string = aiFoundryProject.name
@description('Identity principal ID for the deployed AI Foundry Project resource.')
output identityPrincipalId string = identityId == null ? aiFoundryProject.identity.principalId : identityId!
@description('Serverless model deployments for the AI Foundry Project resource.')
output serverlessModelDeployments serverlessModelDeploymentOutputInfo[] = [
  for (item, index) in serverlessModels: {
    id: serverlessModelEndpoints[index].outputs.id
    name: serverlessModelEndpoints[index].outputs.name
    endpoint: serverlessModelEndpoints[index].outputs.endpoint
    primaryKeySecretName: serverlessModelEndpoints[index].outputs.primaryKeySecretName
    secondaryKeySecretName: serverlessModelEndpoints[index].outputs.secondaryKeySecretName
  }
]
