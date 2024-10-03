import { roleAssignmentInfo } from '../security/managed-identity.bicep'

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
@description('Role assignments to create for the Key Vault.')
param roleAssignments roleAssignmentInfo[] = []

resource keyVault 'Microsoft.KeyVault/vaults@2024-04-01-preview' = {
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
      defaultAction: 'Allow'
      bypass: 'AzureServices'
      ipRules: []
      virtualNetworkRules: []
    }
    enableSoftDelete: enableSoftDelete
    enabledForTemplateDeployment: true
    enableRbacAuthorization: true
    enablePurgeProtection: enablePurgeProtection
    softDeleteRetentionInDays: retentionInDays
  }
}

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

@description('ID for the deployed Key Vault resource.')
output id string = keyVault.id
@description('Name for the deployed Key Vault resource.')
output name string = keyVault.name
@description('URI for the deployed Key Vault resource.')
output uri string = keyVault.properties.vaultUri
