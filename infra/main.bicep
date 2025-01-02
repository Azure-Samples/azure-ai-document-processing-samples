import { modelDeploymentInfo, raiPolicyInfo } from './ai_ml/ai-services.bicep'
import { identityInfo } from './security/managed-identity.bicep'

targetScope = 'subscription'

@minLength(1)
@maxLength(64)
@description('Name of the workload which is used to generate a short unique hash used in all resources.')
param workloadName string

@minLength(1)
@description('Primary location for all resources.')
param location string

@description('Name of the resource group. If empty, a unique name will be generated.')
param resourceGroupName string = ''

@description('Tags for all resources.')
param tags object = {
  WorkloadName: workloadName
  Environment: 'Dev'
}

@description('Responsible AI policies for the Azure AI Services instance.')
param raiPolicies raiPolicyInfo[] = [
  {
    name: workloadName
    mode: 'Blocking'
    prompt: {}
    completion: {}
  }
]

@description('Identities to assign roles to.')
param identities identityInfo[] = []

var abbrs = loadJsonContent('./abbreviations.json')
var roles = loadJsonContent('./roles.json')
var resourceToken = toLower(uniqueString(subscription().id, workloadName, location))

resource contributorRole 'Microsoft.Authorization/roleDefinitions@2022-05-01-preview' existing = {
  scope: resourceGroup
  name: roles.general.contributor
}

resource resourceGroup 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: !empty(resourceGroupName) ? resourceGroupName : '${abbrs.managementGovernance.resourceGroup}${workloadName}'
  location: location
  tags: union(tags, {})
}

var contributorIdentityAssignments = [
  for identity in identities: {
    principalId: identity.principalId
    roleDefinitionId: contributorRole.id
    principalType: identity.principalType
  }
]

module resourceGroupRoleAssignment './security/resource-group-role-assignment.bicep' = {
  name: '${resourceGroup.name}-role-assignment'
  scope: resourceGroup
  params: {
    roleAssignments: concat(contributorIdentityAssignments, [])
  }
}

resource keyVaultAdministratorRole 'Microsoft.Authorization/roleDefinitions@2022-05-01-preview' existing = {
  scope: resourceGroup
  name: roles.security.keyVaultAdministrator
}

var keyVaultAdministratorIdentityAssignments = [
  for identity in identities: {
    principalId: identity.principalId
    roleDefinitionId: keyVaultAdministratorRole.id
    principalType: identity.principalType
  }
]

var keyVaultName = '${abbrs.security.keyVault}${resourceToken}'
module keyVault './security/key-vault.bicep' = {
  name: keyVaultName
  scope: resourceGroup
  params: {
    name: keyVaultName
    location: location
    tags: union(tags, {})
    roleAssignments: concat(keyVaultAdministratorIdentityAssignments, [])
  }
}

var logAnalyticsWorkspaceName = '${abbrs.managementGovernance.logAnalyticsWorkspace}${resourceToken}'
module logAnalyticsWorkspace './management_governance/log-analytics-workspace.bicep' = {
  name: logAnalyticsWorkspaceName
  scope: resourceGroup
  params: {
    name: logAnalyticsWorkspaceName
    location: location
    tags: union(tags, {})
  }
}

var applicationInsightsName = '${abbrs.managementGovernance.applicationInsights}${resourceToken}'
module applicationInsights './management_governance/application-insights.bicep' = {
  name: applicationInsightsName
  scope: resourceGroup
  params: {
    name: applicationInsightsName
    location: location
    tags: union(tags, {})
    logAnalyticsWorkspaceName: logAnalyticsWorkspace.outputs.name
  }
}

resource cognitiveServicesUserRole 'Microsoft.Authorization/roleDefinitions@2022-05-01-preview' existing = {
  scope: resourceGroup
  name: roles.ai.cognitiveServicesUser
}

resource cognitiveServicesContributorRole 'Microsoft.Authorization/roleDefinitions@2022-05-01-preview' existing = {
  scope: resourceGroup
  name: roles.ai.cognitiveServicesContributor
}

resource cognitiveServicesOpenAIContributorRole 'Microsoft.Authorization/roleDefinitions@2022-05-01-preview' existing = {
  scope: resourceGroup
  name: roles.ai.cognitiveServicesOpenAIContributor
}

resource cognitiveServicesOpenAIUserRole 'Microsoft.Authorization/roleDefinitions@2022-05-01-preview' existing = {
  scope: resourceGroup
  name: roles.ai.cognitiveServicesOpenAIUser
}

var cognitiveServicesUserRoleAssignments = [
  for identity in identities: {
    principalId: identity.principalId
    roleDefinitionId: cognitiveServicesUserRole.id
    principalType: identity.principalType
  }
]

var cognitiveServicesContributorRoleAssignments = [
  for identity in identities: {
    principalId: identity.principalId
    roleDefinitionId: cognitiveServicesContributorRole.id
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

var cognitiveServicesOpenAIContributorRoleAssignments = [
  for identity in identities: {
    principalId: identity.principalId
    roleDefinitionId: cognitiveServicesOpenAIContributorRole.id
    principalType: identity.principalType
  }
]

var gpt4oModelDeploymentName = 'gpt-4o'
var gpt4oMiniModelDeploymentName = 'gpt-4o-mini'
var textEmbeddingModelDeploymentName = 'text-embedding-3-large'

var aiServicesName = '${abbrs.ai.aiServices}${resourceToken}'
module aiServices './ai_ml/ai-services.bicep' = {
  name: aiServicesName
  scope: resourceGroup
  params: {
    name: aiServicesName
    location: location
    tags: union(tags, {})
    raiPolicies: raiPolicies
    deployments: [
      {
        name: gpt4oModelDeploymentName
        model: {
          format: 'OpenAI'
          name: 'gpt-4o'
          version: '2024-11-20'
        }
        sku: {
          name: 'GlobalStandard'
          capacity: 10
        }
        raiPolicyName: workloadName
        versionUpgradeOption: 'OnceCurrentVersionExpired'
      }
      {
        name: gpt4oMiniModelDeploymentName
        model: {
          format: 'OpenAI'
          name: 'gpt-4o-mini'
          version: '2024-07-18'
        }
        sku: {
          name: 'GlobalStandard'
          capacity: 10
        }
        raiPolicyName: workloadName
        versionUpgradeOption: 'OnceCurrentVersionExpired'
      }
      {
        name: textEmbeddingModelDeploymentName
        model: {
          format: 'OpenAI'
          name: 'text-embedding-3-large'
          version: '1'
        }
        sku: {
          name: 'Standard'
          capacity: 100
        }
        raiPolicyName: workloadName
        versionUpgradeOption: 'OnceCurrentVersionExpired'
      }
    ]
    roleAssignments: concat(
      cognitiveServicesUserRoleAssignments,
      cognitiveServicesContributorRoleAssignments,
      cognitiveServicesOpenAIUserRoleAssignments,
      cognitiveServicesOpenAIContributorRoleAssignments,
      []
    )
  }
}

// Require self-referencing role assignment for AI Services identity to access Azure OpenAI.
module aiServicesRoleAssignment './security/resource-role-assignment.json' = {
  name: '${abbrs.ai.aiServices}${resourceToken}-role-assignment'
  scope: resourceGroup
  params: {
    resourceId: aiServices.outputs.id
    roleAssignments: [
      {
        principalId: aiServices.outputs.principalId
        roleDefinitionId: cognitiveServicesUserRole.id
        principalType: 'ServicePrincipal'
      }
    ]
  }
}

// Storage account roles required for using Prompt Flow in AI Hubs
resource storageAccountContributorRole 'Microsoft.Authorization/roleDefinitions@2022-05-01-preview' existing = {
  scope: resourceGroup
  name: roles.storage.storageAccountContributor
}

resource storageBlobDataContributorRole 'Microsoft.Authorization/roleDefinitions@2022-05-01-preview' existing = {
  scope: resourceGroup
  name: roles.storage.storageBlobDataContributor
}

resource storageFileDataPrivilegedContributorRole 'Microsoft.Authorization/roleDefinitions@2022-05-01-preview' existing = {
  scope: resourceGroup
  name: roles.storage.storageFileDataPrivilegedContributor
}

resource storageTableDataContributorRole 'Microsoft.Authorization/roleDefinitions@2022-05-01-preview' existing = {
  scope: resourceGroup
  name: roles.storage.storageTableDataContributor
}

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

var storageAccountName = '${abbrs.storage.storageAccount}${resourceToken}'
module storageAccount './storage/storage-account.bicep' = {
  name: storageAccountName
  scope: resourceGroup
  params: {
    name: storageAccountName
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
          principalId: aiServices.outputs.principalId
          roleDefinitionId: storageBlobDataContributorRole.id
          principalType: 'ServicePrincipal'
        }
      ]
    )
  }
}

resource azureMLDataScientistRole 'Microsoft.Authorization/roleDefinitions@2022-05-01-preview' existing = {
  scope: resourceGroup
  name: roles.ai.azureMLDataScientist
}

var azureMLDataScientistRoleAssignments = [
  for identity in identities: {
    principalId: identity.principalId
    roleDefinitionId: azureMLDataScientistRole.id
    principalType: identity.principalType
  }
]

var aiHubName = '${abbrs.ai.aiHub}${resourceToken}'
module aiHub './ai_ml/ai-hub.bicep' = {
  name: aiHubName
  scope: resourceGroup
  params: {
    name: aiHubName
    friendlyName: 'Hub - AI Document Processing'
    descriptionInfo: 'Generated by the AI Document Processing Samples'
    location: location
    tags: union(tags, {})
    storageAccountId: storageAccount.outputs.id
    keyVaultId: keyVault.outputs.id
    applicationInsightsId: applicationInsights.outputs.id
    aiServicesName: aiServices.outputs.name
    roleAssignments: concat(azureMLDataScientistRoleAssignments, [])
  }
}

var phiModelDeploymentName = 'phi-35-moe-${resourceToken}'

var aiHubProjectName = '${abbrs.ai.aiHubProject}${resourceToken}'
module aiHubProject './ai_ml/ai-hub-project.bicep' = {
  name: aiHubProjectName
  scope: resourceGroup
  params: {
    name: aiHubProjectName
    friendlyName: 'Project - AI Document Processing'
    descriptionInfo: 'Generated by the AI Document Processing Samples'
    location: location
    tags: union(tags, {})
    aiHubName: aiHub.outputs.name
    serverlessModels: [
      {
        name: phiModelDeploymentName
        model: {
          name: 'Phi-35-moe-instruct'
        }
        keyVaultConfig: {
          name: keyVault.outputs.name
          primaryKeySecretName: 'Phi-35-MoE-PrimaryKey'
          secondaryKeySecretName: 'Phi-35-MoE-SecondaryKey'
        }
      }
    ]
    roleAssignments: concat(azureMLDataScientistRoleAssignments, [])
  }
}

output subscriptionInfo object = {
  id: subscription().subscriptionId
  tenantId: subscription().tenantId
}

output resourceGroupInfo object = {
  id: resourceGroup.id
  name: resourceGroup.name
  location: resourceGroup.location
  workloadName: workloadName
}

output storageAccountInfo object = {
  id: storageAccount.outputs.id
  name: storageAccount.outputs.name
  location: location
}

output keyVaultInfo object = {
  id: keyVault.outputs.id
  name: keyVault.outputs.name
  uri: keyVault.outputs.uri
  location: location
}

output aiModelsInfo object = {
  openAIEndpoint: aiServices.outputs.openAIEndpoint
  aiServicesEndpoint: aiServices.outputs.endpoint
  gpt4oModelDeploymentName: gpt4oModelDeploymentName
  gpt4oMiniModelDeploymentName: gpt4oMiniModelDeploymentName
  textEmbeddingModelDeploymentName: textEmbeddingModelDeploymentName
  phi3Endpoint: aiHubProject.outputs.serverlessModelDeployments[0].endpoint
  phi3PrimaryKeySecretName: aiHubProject.outputs.serverlessModelDeployments[0].primaryKeySecretName
}
