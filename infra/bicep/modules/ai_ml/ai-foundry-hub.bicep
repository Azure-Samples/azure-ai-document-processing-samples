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

@description('Friendly name for the AI Foundry Hub.')
param friendlyName string = name
@description('Description for the AI Foundry Hub.')
param descriptionInfo string = 'Azure AI Foundry Hub'
@description('Isolation mode for the AI Foundry Hub.')
@allowed([
  'AllowInternetOutbound'
  'AllowOnlyApprovedOutbound'
  'Disabled'
])
param isolationMode string = 'AllowInternetOutbound'
@description('Whether to enable public network access. Defaults to Enabled.')
param publicNetworkAccess 'Enabled' | 'Disabled' | 'SecuredByPerimeter' = 'Enabled'
@description('Whether or not to use credentials for the system datastores of the workspace. Defaults to identity.')
@allowed([
  'accessKey'
  'identity'
])
param systemDatastoresAuthMode string = 'identity'
@description('ID for the Storage Account associated with the AI Foundry Hub.')
param storageAccountId string
@description('ID for the Key Vault associated with the AI Foundry Hub.')
param keyVaultId string
@description('ID for the Application Insights associated with the AI Foundry Hub.')
param applicationInsightsId string
@description('ID for the Container Registry associated with the AI Foundry Hub.')
param containerRegistryId string?
@description('ID for the Managed Identity associated with the AI Foundry Hub. Defaults to the system-assigned identity.')
param identityId string?
@description('Name for the AI Services resource to connect to.')
param aiServicesName string
@description('Serverless model deployments for the AI Foundry Hub.')
param serverlessModels serverlessModelDeploymentInfo[] = []
@description('Resource connections associated with the AI Foundry Hub.')
param connections connectionInfo[] = []
@description('Role assignments to create for the AI Foundry Hub instance.')
param roleAssignments roleAssignmentInfo[] = []
@description('Name of the Log Analytics Workspace to use for diagnostic settings.')
param logAnalyticsWorkspaceName string?
@description('Diagnostic settings to configure for the AI Foundry Hub instance. Defaults to all logs and metrics.')
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

resource aiServices 'Microsoft.CognitiveServices/accounts@2025-04-01-preview' existing = {
  name: aiServicesName
}

resource aiFoundryHub 'Microsoft.MachineLearningServices/workspaces@2025-01-01-preview' = {
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

  resource aiServicesConnection 'connections@2025-01-01-preview' = {
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

module aiFoundryHubConnections 'ai-foundry-hub-connection.bicep' = [
  for connection in connections: {
    name: connection.name
    params: {
      aiFoundryName: aiFoundryHub.name
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
      aiFoundryName: aiFoundryHub.name
      model: serverlessModel.model
      keyVaultConfig: serverlessModel.keyVaultConfig
    }
  }
]

resource assignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = [
  for roleAssignment in roleAssignments: {
    name: guid(aiFoundryHub.id, roleAssignment.principalId, roleAssignment.roleDefinitionId)
    scope: aiFoundryHub
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

resource aiFoundryHubDiagnosticSettings 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = if (logAnalyticsWorkspaceName != null) {
  name: '${aiFoundryHub.name}-diagnostic-settings'
  scope: aiFoundryHub
  properties: {
    workspaceId: logAnalyticsWorkspace.id
    logs: diagnosticSettings!.logs
    metrics: diagnosticSettings!.metrics
  }
}

// Outputs

@description('ID for the deployed AI Foundry Hub resource.')
output id string = aiFoundryHub.id
@description('Name for the deployed AI Foundry Hub resource.')
output name string = aiFoundryHub.name
@description('Identity principal ID for the deployed AI Foundry Hub resource.')
output identityPrincipalId string = identityId == null ? aiFoundryHub.identity.principalId : identityId!
@description('AI Services connection name for the deployed AI Foundry Hub resource.')
output aiServicesConnectionName string = aiFoundryHub::aiServicesConnection.name
@description('OpenAI specific connection name for the deployed AI Foundry Hub resource.')
output openAIServicesConnectionName string = '${aiFoundryHub::aiServicesConnection.name}_aoai'
@description('Serverless model deployments for the AI Foundry Hub resource.')
output serverlessModelDeployments serverlessModelDeploymentOutputInfo[] = [
  for (item, index) in serverlessModels: {
    id: serverlessModelEndpoints[index].outputs.id
    name: serverlessModelEndpoints[index].outputs.name
    endpoint: serverlessModelEndpoints[index].outputs.endpoint
    primaryKeySecretName: serverlessModelEndpoints[index].outputs.primaryKeySecretName
    secondaryKeySecretName: serverlessModelEndpoints[index].outputs.secondaryKeySecretName
  }
]
