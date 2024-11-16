import { raiPolicyInfo } from './ai_ml/ai-services.bicep'

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

@description('Principal ID of the user that will be granted permission to access services.')
param userPrincipalId string

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

var aiStudioIdentityResourceToken = toLower(uniqueString(resourceToken, 'ai-studio'))
var aiStudioIdentityName = '${abbrs.security.managedIdentity}${aiStudioIdentityResourceToken}'
module aiStudioIdentity './security/managed-identity.bicep' = {
  name: aiStudioIdentityName
  scope: resourceGroup
  params: {
    name: aiStudioIdentityName
    location: location
    tags: union(tags, { IdentityFor: aiStudioHubName })
  }
}

module resouceGroupRoleAssignment './security/resource-group-role-assignment.bicep' = {
  name: '${resourceGroup.name}-role-assignment'
  scope: resourceGroup
  params: {
    roleAssignments: [
      {
        principalId: userPrincipalId
        roleDefinitionId: contributorRole.id
        principalType: 'User'
      }
      {
        principalId: aiStudioIdentity.outputs.principalId
        roleDefinitionId: contributorRole.id
        principalType: 'ServicePrincipal'
      }
    ]
  }
}

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
    roleAssignments: [
      {
        principalId: aiStudioIdentity.outputs.principalId
        roleDefinitionId: storageAccountContributorRole.id
        principalType: 'ServicePrincipal'
      }
      {
        principalId: aiStudioIdentity.outputs.principalId
        roleDefinitionId: storageBlobDataContributorRole.id
        principalType: 'ServicePrincipal'
      }
      {
        principalId: aiStudioIdentity.outputs.principalId
        roleDefinitionId: storageFileDataPrivilegedContributorRole.id
        principalType: 'ServicePrincipal'
      }
      {
        principalId: aiStudioIdentity.outputs.principalId
        roleDefinitionId: storageTableDataContributorRole.id
        principalType: 'ServicePrincipal'
      }
      {
        principalId: userPrincipalId
        roleDefinitionId: storageAccountContributorRole.id
        principalType: 'User'
      }
      {
        principalId: userPrincipalId
        roleDefinitionId: storageBlobDataContributorRole.id
        principalType: 'User'
      }
      {
        principalId: userPrincipalId
        roleDefinitionId: storageFileDataPrivilegedContributorRole.id
        principalType: 'User'
      }
      {
        principalId: userPrincipalId
        roleDefinitionId: storageTableDataContributorRole.id
        principalType: 'User'
      }
    ]
  }
}

resource keyVaultAdministratorRole 'Microsoft.Authorization/roleDefinitions@2022-05-01-preview' existing = {
  scope: resourceGroup
  name: roles.security.keyVaultAdministrator
}

var keyVaultName = '${abbrs.security.keyVault}${resourceToken}'
module keyVault './security/key-vault.bicep' = {
  name: keyVaultName
  scope: resourceGroup
  params: {
    name: keyVaultName
    location: location
    tags: union(tags, {})
    roleAssignments: [
      {
        principalId: aiStudioIdentity.outputs.principalId
        roleDefinitionId: keyVaultAdministratorRole.id
        principalType: 'ServicePrincipal'
      }
      {
        principalId: userPrincipalId
        roleDefinitionId: keyVaultAdministratorRole.id
        principalType: 'User'
      }
    ]
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

resource acrPushRole 'Microsoft.Authorization/roleDefinitions@2022-04-01' existing = {
  scope: resourceGroup
  name: roles.containers.acrPush
}

resource acrPullRole 'Microsoft.Authorization/roleDefinitions@2022-04-01' existing = {
  scope: resourceGroup
  name: roles.containers.acrPull
}

var containerRegistryName = '${abbrs.containers.containerRegistry}${resourceToken}'
module containerRegistry './containers/container-registry.bicep' = {
  name: containerRegistryName
  scope: resourceGroup
  params: {
    name: containerRegistryName
    location: location
    tags: union(tags, {})
    sku: {
      name: 'Basic'
    }
    adminUserEnabled: true
    roleAssignments: [
      {
        principalId: aiStudioIdentity.outputs.principalId
        roleDefinitionId: acrPushRole.id
        principalType: 'ServicePrincipal'
      }
      {
        principalId: aiStudioIdentity.outputs.principalId
        roleDefinitionId: acrPullRole.id
        principalType: 'ServicePrincipal'
      }
      {
        principalId: userPrincipalId
        roleDefinitionId: acrPushRole.id
        principalType: 'User'
      }
      {
        principalId: userPrincipalId
        roleDefinitionId: acrPullRole.id
        principalType: 'User'
      }
    ]
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

var gpt4oModelDeploymentName = 'gpt-4o'
var gpt4oMiniDeploymentName = 'gpt-4o-mini'
var textEmbeddingModelDeploymentName = 'text-embedding-3-large'

var aiServicesName = '${abbrs.ai.aiServices}${resourceToken}'
module aiServices './ai_ml/ai-services.bicep' = {
  name: aiServicesName
  scope: resourceGroup
  params: {
    name: aiServicesName
    location: location
    tags: union(tags, {})
    identityId: aiStudioIdentity.outputs.id
    raiPolicies: [
      {
        name: workloadName
        mode: 'Blocking'
        prompt: {}
        completion: {}
      }
    ]
    deployments: [
      {
        name: gpt4oModelDeploymentName
        model: {
          format: 'OpenAI'
          name: 'gpt-4o'
          version: '2024-08-06'
        }
        sku: {
          name: 'GlobalStandard'
          capacity: 10
        }
        raiPolicyName: workloadName
        versionUpgradeOption: 'OnceCurrentVersionExpired'
      }
      {
        name: gpt4oMiniDeploymentName
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
          capacity: 115
        }
        raiPolicyName: workloadName
        versionUpgradeOption: 'OnceCurrentVersionExpired'
      }
    ]
    roleAssignments: [
      {
        principalId: aiStudioIdentity.outputs.principalId
        roleDefinitionId: cognitiveServicesUserRole.id
        principalType: 'ServicePrincipal'
      }
      {
        principalId: aiStudioIdentity.outputs.principalId
        roleDefinitionId: cognitiveServicesContributorRole.id
        principalType: 'ServicePrincipal'
      }
      {
        principalId: aiStudioIdentity.outputs.principalId
        roleDefinitionId: cognitiveServicesOpenAIContributorRole.id
        principalType: 'ServicePrincipal'
      }
      {
        principalId: userPrincipalId
        roleDefinitionId: cognitiveServicesUserRole.id
        principalType: 'User'
      }
      {
        principalId: userPrincipalId
        roleDefinitionId: cognitiveServicesContributorRole.id
        principalType: 'User'
      }
      {
        principalId: userPrincipalId
        roleDefinitionId: cognitiveServicesOpenAIContributorRole.id
        principalType: 'User'
      }
    ]
  }
}

resource azureMLDataScientistRole 'Microsoft.Authorization/roleDefinitions@2022-05-01-preview' existing = {
  scope: resourceGroup
  name: roles.ai.azureMLDataScientist
}

var aiStudioHubName = '${abbrs.ai.aiHub}${resourceToken}'
module aiStudioHub './ai_ml/ai-hub.bicep' = {
  name: aiStudioHubName
  scope: resourceGroup
  params: {
    name: aiStudioHubName
    friendlyName: 'Hub - Document Data Extraction'
    descriptionInfo: 'Generated for Document Data Extraction demos'
    location: location
    tags: union(tags, {})
    identityId: aiStudioIdentity.outputs.id
    storageAccountId: storageAccount.outputs.id
    keyVaultId: keyVault.outputs.id
    applicationInsightsId: applicationInsights.outputs.id
    containerRegistryId: containerRegistry.outputs.id
    aiServicesName: aiServices.outputs.name
    roleAssignments: [
      {
        principalId: aiStudioIdentity.outputs.principalId
        roleDefinitionId: azureMLDataScientistRole.id
        principalType: 'ServicePrincipal'
      }
      {
        principalId: userPrincipalId
        roleDefinitionId: azureMLDataScientistRole.id
        principalType: 'User'
      }
    ]
  }
}

var phiModelDeploymentName = 'phi-35-moe-${resourceToken}'

var aiStudioHubProjectName = '${abbrs.ai.aiHubProject}${workloadName}'
module aiStudioHubProject './ai_ml/ai-hub-project.bicep' = {
  name: aiStudioHubProjectName
  scope: resourceGroup
  params: {
    name: aiStudioHubProjectName
    friendlyName: 'Project - Document Data Extraction'
    descriptionInfo: 'Generated for Document Data Extraction demos'
    location: location
    tags: union(tags, {})
    identityId: aiStudioIdentity.outputs.id
    aiHubName: aiStudioHub.outputs.name
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
    roleAssignments: [
      {
        principalId: aiStudioIdentity.outputs.principalId
        roleDefinitionId: azureMLDataScientistRole.id
        principalType: 'ServicePrincipal'
      }
      {
        principalId: userPrincipalId
        roleDefinitionId: azureMLDataScientistRole.id
        principalType: 'User'
      }
    ]
  }
}

output subscriptionInfo object = {
  id: subscription().subscriptionId
  tenantId: subscription().tenantId
}

output resourceGroupInfo object = {
  name: resourceGroup.name
  location: resourceGroup.location
  workloadName: workloadName
}

output managedIdentityInfo object = {
  id: aiStudioIdentity.outputs.id
  name: aiStudioIdentity.outputs.name
  principalId: aiStudioIdentity.outputs.principalId
  clientId: aiStudioIdentity.outputs.clientId
}

output storageAccountInfo object = {
  name: storageAccount.outputs.name
  location: location
}

output keyVaultInfo object = {
  name: keyVault.outputs.name
  location: location
}

output aiModelsInfo object = {
  openAIEndpoint: aiServices.outputs.openAIEndpoint
  aiServicesEndpoint: aiServices.outputs.endpoint
  gpt4oModelDeploymentName: gpt4oModelDeploymentName
  textEmbeddingModelDeploymentName: textEmbeddingModelDeploymentName
  phi3Endpoint: aiStudioHubProject.outputs.serverlessModelDeployments[0].endpoint
  phi3PrimaryKeySecretName: aiStudioHubProject.outputs.serverlessModelDeployments[0].primaryKeySecretName
}
