import { modelDeploymentInfo, raiPolicyInfo } from './modules/ai_ml/ai-services.bicep'
import { serverlessModelDeploymentInfo } from './modules/ai_ml/ai-foundry-model-serverless-endpoint.bicep'
import { identityInfo } from './modules/security/managed-identity.bicep'

@minLength(1)
@maxLength(48)
@description('Name of the workload which is used to generate a short unique hash used in all resources.')
param workloadName string

@minLength(1)
@description('Primary location for all resources.')
param location string

@description('Tags for all resources. Define your tagging strategy using https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-tagging.')
param tags object = {
  WorkloadName: workloadName
  DataClassification: 'General'
  Criticality: 'Medium'
  Environment: 'Dev'
  RepositoryUrl: 'https://github.com/azure-samples/azure-ai-document-processing-samples'
}

@description('Name of the Key Vault to deploy. If left empty, a name will be generated using Azure CAF best practices.')
param keyVaultName string = ''

@description('Name of the Log Analytics Workspace to deploy. If left empty, a name will be generated using Azure CAF best practices.')
param logAnalyticsWorkspaceName string = ''

@description('Name of the Application Insights instance to deploy. If left empty, a name will be generated using Azure CAF best practices.')
param applicationInsightsName string = ''

@description('Name of the Azure AI Services instance to deploy. If left empty, a name will be generated using Azure CAF best practices.')
param aiServicesName string = ''

@description('Name of the Storage Account to deploy. If left empty, a name will be generated using Azure CAF best practices.')
param storageAccountName string = ''

@description('Name of the Azure AI Foundry Hub to deploy. If left empty, a name will be generated using Azure CAF best practices.')
param aiFoundryHubName string = ''

@description('Name of the Azure AI Foundry Project to deploy. If left empty, a name will be generated using Azure CAF best practices.')
param aiFoundryProjectName string = ''

@description('Identities to assign roles to.')
param identities identityInfo[] = []

@description('Responsible AI policies for the Azure AI Services instance.')
param raiPolicies raiPolicyInfo[] = [
  {
    name: workloadName
    mode: 'Blocking'
    prompt: {}
    completion: {}
  }
]

@description('Model deployment for Azure OpenAI chat completion.')
param chatModelDeployment modelDeploymentInfo?

@description('Model deployment for Azure OpenAI text embedding.')
param textEmbeddingModelDeployment modelDeploymentInfo?

@description('Model deployment for Azure AI chat completion with Phi.')
param phiModelDeployment serverlessModelDeploymentInfo?

// Variables

var abbrs = loadJsonContent('./abbreviations.json')
var roles = loadJsonContent('./roles.json')
var resourceToken = toLower(uniqueString(subscription().id, workloadName, location))

var _keyVaultName = !empty(keyVaultName) ? keyVaultName : '${abbrs.security.keyVault}${resourceToken}'

var _logAnalyticsWorkspaceName = !empty(logAnalyticsWorkspaceName)
  ? logAnalyticsWorkspaceName
  : '${abbrs.managementGovernance.logAnalyticsWorkspace}${resourceToken}'

var _applicationInsightsName = !empty(applicationInsightsName)
  ? applicationInsightsName
  : '${abbrs.managementGovernance.applicationInsights}${resourceToken}'

var _aiServicesName = !empty(aiServicesName) ? aiServicesName : '${abbrs.ai.aiServices}${resourceToken}'

var _aiServicesLocation = chatModelDeployment.?model.name == 'model-router'
  ? (location == 'eastus2' || location == 'swedencentral' ? location : 'eastus2')
  : location

var _storageAccountName = !empty(storageAccountName)
  ? storageAccountName
  : '${abbrs.storage.storageAccount}${resourceToken}'

var _aiFoundryHubName = !empty(aiFoundryHubName) ? aiFoundryHubName : '${abbrs.ai.aiFoundryHub}${resourceToken}'

var _aiFoundryProjectName = !empty(aiFoundryProjectName)
  ? aiFoundryProjectName
  : '${abbrs.ai.aiFoundryProject}${resourceToken}'

var _chatModelDeployment = chatModelDeployment ?? {
  name: 'gpt-4.1'
  model: { format: 'OpenAI', name: 'gpt-4.1', version: '2025-04-14' }
  sku: { name: 'GlobalStandard', capacity: 50 }
  raiPolicyName: workloadName
  versionUpgradeOption: 'OnceCurrentVersionExpired'
}

var _textEmbeddingModelDeployment = textEmbeddingModelDeployment ?? {
  name: 'text-embedding-3-large'
  model: { format: 'OpenAI', name: 'text-embedding-3-large', version: '1' }
  sku: { name: 'Standard', capacity: 100 }
  raiPolicyName: workloadName
  versionUpgradeOption: 'OnceCurrentVersionExpired'
}

var _phiModelDeployment = phiModelDeployment ?? {
  name: 'phi-4-${resourceToken}'
  model: { name: 'Phi-4' }
  keyVaultConfig: {
    name: _keyVaultName
    primaryKeySecretName: 'Phi-4-PrimaryKey'
    secondaryKeySecretName: 'Phi-4-SecondaryKey'
  }
}

var contributorIdentityAssignments = [
  for identity in identities: {
    principalId: identity.principalId
    roleDefinitionId: contributorRole.id
    principalType: identity.principalType
  }
]

var keyVaultSecretsUserIdentityAssignments = [
  for identity in identities: {
    principalId: identity.principalId
    roleDefinitionId: keyVaultSecretsUserRole.id
    principalType: identity.principalType
  }
]

var cognitiveServicesUserRoleAssignments = [
  for identity in identities: {
    principalId: identity.principalId
    roleDefinitionId: cognitiveServicesUserRole.id
    principalType: identity.principalType
  }
]

var cognitiveServicesOpenAIUserRoleAssignments = [
  for identity in identities: {
    principalId: identity.principalId
    roleDefinitionId: cognitiveServicesOpenAIUserRole.id
    principalType: identity.principalType
  }
]

var azureAIDeveloperRoleAssignments = [
  for identity in identities: {
    principalId: identity.principalId
    roleDefinitionId: azureAIDeveloperRole.id
    principalType: identity.principalType
  }
]

var storageAccountContributorIdentityAssignments = [
  for identity in identities: {
    principalId: identity.principalId
    roleDefinitionId: storageAccountContributorRole.id
    principalType: identity.principalType
  }
]

var storageBlobDataContributorIdentityAssignments = [
  for identity in identities: {
    principalId: identity.principalId
    roleDefinitionId: storageBlobDataContributorRole.id
    principalType: identity.principalType
  }
]

var storageFileDataPrivilegedContributorIdentityAssignments = [
  for identity in identities: {
    principalId: identity.principalId
    roleDefinitionId: storageFileDataPrivilegedContributorRole.id
    principalType: identity.principalType
  }
]

var storageTableDataContributorIdentityAssignments = [
  for identity in identities: {
    principalId: identity.principalId
    roleDefinitionId: storageTableDataContributorRole.id
    principalType: identity.principalType
  }
]

var azureMLDataScientistRoleAssignments = [
  for identity in identities: {
    principalId: identity.principalId
    roleDefinitionId: azureMLDataScientistRole.id
    principalType: identity.principalType
  }
]

// Deployments

resource contributorRole 'Microsoft.Authorization/roleDefinitions@2022-05-01-preview' existing = {
  name: roles.general.contributor
}

module resourceGroupRoleAssignment './modules/security/resource-group-role-assignment.bicep' = {
  name: '${resourceGroup().name}-role'
  params: {
    roleAssignments: concat(contributorIdentityAssignments, [])
  }
}

resource keyVaultSecretsUserRole 'Microsoft.Authorization/roleDefinitions@2022-05-01-preview' existing = {
  name: roles.security.keyVaultSecretsUser
}

module keyVault './modules/security/key-vault.bicep' = {
  name: _keyVaultName
  params: {
    name: _keyVaultName
    location: location
    tags: union(tags, {})
    roleAssignments: concat(keyVaultSecretsUserIdentityAssignments, [])
    publicNetworkAccess: 'Enabled'
    networkAclsDefaultAction: 'Allow'
  }
}

module logAnalyticsWorkspace './modules/management_governance/log-analytics-workspace.bicep' = {
  name: _logAnalyticsWorkspaceName
  params: {
    name: _logAnalyticsWorkspaceName
    location: location
    tags: union(tags, {})
  }
}

module applicationInsights './modules/management_governance/application-insights.bicep' = {
  name: _applicationInsightsName
  params: {
    name: _applicationInsightsName
    location: location
    tags: union(tags, {})
    logAnalyticsWorkspaceName: logAnalyticsWorkspace.outputs.name
  }
}

resource cognitiveServicesUserRole 'Microsoft.Authorization/roleDefinitions@2022-05-01-preview' existing = {
  name: roles.ai.cognitiveServicesUser
}

resource cognitiveServicesOpenAIUserRole 'Microsoft.Authorization/roleDefinitions@2022-05-01-preview' existing = {
  name: roles.ai.cognitiveServicesOpenAIUser
}

resource azureAIDeveloperRole 'Microsoft.Authorization/roleDefinitions@2022-05-01-preview' existing = {
  name: roles.ai.azureAIDeveloper
}

module aiServices './modules/ai_ml/ai-services.bicep' = {
  name: _aiServicesName
  params: {
    name: _aiServicesName
    location: _aiServicesLocation
    tags: union(tags, {})
    raiPolicies: raiPolicies
    logAnalyticsWorkspaceName: logAnalyticsWorkspace.outputs.name
    deployments: [
      _chatModelDeployment
      _textEmbeddingModelDeployment
    ]
    roleAssignments: concat(
      cognitiveServicesUserRoleAssignments,
      cognitiveServicesOpenAIUserRoleAssignments,
      azureAIDeveloperRoleAssignments,
      []
    )
    publicNetworkAccess: 'Enabled'
    networkAclsDefaultAction: 'Allow'
  }
}

// Require self-referencing role assignment for AI Services identity to access Azure OpenAI.
module aiServicesRoleAssignment './modules/security/resource-role-assignment.json' = {
  name: '${_aiServicesName}-role'
  params: {
    resourceId: aiServices.outputs.id
    roleAssignments: [
      {
        principalId: aiServices.outputs.identityPrincipalId
        roleDefinitionId: cognitiveServicesUserRole.id
        principalType: 'ServicePrincipal'
      }
      {
        principalId: aiServices.outputs.identityPrincipalId
        roleDefinitionId: cognitiveServicesOpenAIUserRole.id
        principalType: 'ServicePrincipal'
      }
      {
        principalId: aiServices.outputs.identityPrincipalId
        roleDefinitionId: azureAIDeveloperRole.id
        principalType: 'ServicePrincipal'
      }
    ]
  }
}

// Storage account roles required for AI Foundry.
resource storageAccountContributorRole 'Microsoft.Authorization/roleDefinitions@2022-05-01-preview' existing = {
  name: roles.storage.storageAccountContributor
}

resource storageBlobDataContributorRole 'Microsoft.Authorization/roleDefinitions@2022-05-01-preview' existing = {
  name: roles.storage.storageBlobDataContributor
}

resource storageFileDataPrivilegedContributorRole 'Microsoft.Authorization/roleDefinitions@2022-05-01-preview' existing = {
  name: roles.storage.storageFileDataPrivilegedContributor
}

resource storageTableDataContributorRole 'Microsoft.Authorization/roleDefinitions@2022-05-01-preview' existing = {
  name: roles.storage.storageTableDataContributor
}

module storageAccount './modules/storage/storage-account.bicep' = {
  name: _storageAccountName
  params: {
    name: _storageAccountName
    location: location
    tags: union(tags, {})
    sku: {
      name: 'Standard_LRS'
    }
    roleAssignments: concat(
      storageAccountContributorIdentityAssignments,
      storageBlobDataContributorIdentityAssignments,
      storageFileDataPrivilegedContributorIdentityAssignments,
      storageTableDataContributorIdentityAssignments,
      [
        {
          principalId: aiServices.outputs.identityPrincipalId
          roleDefinitionId: storageBlobDataContributorRole.id
          principalType: 'ServicePrincipal'
        }
      ]
    )
    publicNetworkAccess: 'Enabled'
    networkAclsDefaultAction: 'Allow'
  }
}

resource azureMLDataScientistRole 'Microsoft.Authorization/roleDefinitions@2022-05-01-preview' existing = {
  name: roles.ai.azureMLDataScientist
}

module aiFoundryHub './modules/ai_ml/ai-foundry-hub.bicep' = {
  name: _aiFoundryHubName
  params: {
    name: _aiFoundryHubName
    friendlyName: 'AI Document Processing Hub'
    descriptionInfo: 'Hub for AI services and projects'
    location: location
    tags: union(tags, {})
    storageAccountId: storageAccount.outputs.id
    keyVaultId: keyVault.outputs.id
    applicationInsightsId: applicationInsights.outputs.id
    aiServicesName: aiServices.outputs.name
    roleAssignments: concat(azureMLDataScientistRoleAssignments, [])
  }
}

module aiFoundryProject './modules/ai_ml/ai-foundry-project.bicep' = {
  name: _aiFoundryProjectName
  params: {
    name: _aiFoundryProjectName
    friendlyName: 'AI Document Processing Project'
    descriptionInfo: 'Project resources'
    location: location
    tags: union(tags, {})
    aiFoundryHubName: aiFoundryHub.outputs.name
    serverlessModels: [
      _phiModelDeployment
    ]
    roleAssignments: concat(azureMLDataScientistRoleAssignments, [])
  }
}

// Outputs

output environmentInfo object = {
  azureResourceGroup: resourceGroup().name
  azureStorageAccountName: storageAccount.outputs.name
  azureKeyVaultName: keyVault.outputs.name
  azureAIServicesEndpoint: aiServices.outputs.endpoint
  azureOpenAIEndpoint: aiServices.outputs.openAIEndpoint
  azureOpenAIChatDeployment: _chatModelDeployment.name
  azureOpenAITextEmbeddingDeployment: _textEmbeddingModelDeployment.name
  azureAIPhiEndpoint: aiFoundryProject.outputs.serverlessModelDeployments[0].endpoint
  azureAIPhiPrimaryKeySecretName: aiFoundryProject.outputs.serverlessModelDeployments[0].primaryKeySecretName
}
