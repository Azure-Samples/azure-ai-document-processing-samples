import { roleAssignmentInfo } from '../security/managed-identity.bicep'
import { diagnosticSettingsInfo } from '../management_governance/log-analytics-workspace.bicep'

@description('Name of the resource.')
param name string
@description('Location to deploy the resource. Defaults to the location of the resource group.')
param location string = resourceGroup().location
@description('Tags for the resource.')
param tags object = {}

@description('Key Vault SKU name. Defaults to standard.')
@allowed([
  'standard'
  'premium'
])
param skuName string = 'standard'
@description('Whether soft deletion is enabled. Defaults to true.')
param enableSoftDelete bool = true
@description('Number of days to retain soft-deleted keys, secrets, and certificates. Defaults to 90.')
param retentionInDays int = 90
@description('Whether purge protection is enabled. Defaults to true.')
param enablePurgeProtection bool = true
@description('Whether to enable public network access. Defaults to Enabled.')
param publicNetworkAccess 'Enabled' | 'Disabled' | 'SecuredByPerimeter' = 'Enabled'
@description('Default network access control action when no other rules match. This is only used after the bypass property has been evaluated. Defaults to Allow.')
param networkAclsDefaultAction 'Allow' | 'Deny' = 'Allow'
@description('IP rules for network ACLs.')
param ipRules array = []
@description('Secret Keys to add to App Configuration')
param secureAppSettings keyVaultSecretInfo[] = []
@description('Role assignments to create for the Key Vault.')
param roleAssignments roleAssignmentInfo[] = []
@description('Name of the Log Analytics Workspace to use for diagnostic settings.')
param logAnalyticsWorkspaceName string?
@description('Diagnostic settings to configure for the Key Vault instance. Defaults to all logs and metrics.')
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

resource keyVault 'Microsoft.KeyVault/vaults@2024-12-01-preview' = {
  name: name
  location: location
  tags: tags
  properties: {
    sku: {
      family: 'A'
      name: skuName
    }
    tenantId: subscription().tenantId
    networkAcls: {
      defaultAction: networkAclsDefaultAction
      bypass: 'AzureServices'
      ipRules: ipRules
    }
    enabledForDeployment: true
    enabledForDiskEncryption: true
    enabledForTemplateDeployment: true
    enablePurgeProtection: enablePurgeProtection
    enableRbacAuthorization: true
    enableSoftDelete: enableSoftDelete
    softDeleteRetentionInDays: retentionInDays
    publicNetworkAccess: publicNetworkAccess
  }
}

resource keyVaultSecret 'Microsoft.KeyVault/vaults/secrets@2024-12-01-preview' = [
  for appSetting in secureAppSettings: {
    parent: keyVault
    name: replace(appSetting.name, '_', '-')
    properties: {
      value: appSetting.value
      attributes: {
        enabled: true
      }
    }
  }
]

resource assignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = [
  for roleAssignment in roleAssignments: {
    name: guid(keyVault.id, roleAssignment.principalId, roleAssignment.roleDefinitionId)
    scope: keyVault
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

resource keyVaultDiagnosticSettings 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = if (logAnalyticsWorkspaceName != null) {
  name: '${keyVault.name}-diagnostic-settings'
  scope: keyVault
  properties: {
    workspaceId: logAnalyticsWorkspace.id
    logs: diagnosticSettings!.logs
    metrics: diagnosticSettings!.metrics
  }
}

// Outputs

@description('ID for the deployed Key Vault resource.')
output id string = keyVault.id
@description('Name for the deployed Key Vault resource.')
output name string = keyVault.name
@description('URI for the deployed Key Vault resource.')
output uri string = keyVault.properties.vaultUri
@description('URIs for the deployed Key Vault secrets.')
output secrets array = [
  for (appSetting, i) in secureAppSettings: {
    name: appSetting.name
    value: '{"uri":"${keyVaultSecret[i].properties.secretUri}"}'
  }
]

// Definitions

@export()
@description('Information about app settings for the Key Vault.')
type keyVaultSecretInfo = {
  @description('Name of the key-value pair.')
  name: string
  @description('Value of the key-value pair.')
  value: string
}
