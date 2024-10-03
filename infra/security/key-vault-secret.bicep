@description('Name of the secret.')
param name string

@description('Name of the Key Vault associated with the secret.')
param keyVaultName string
@description('Value of the secret.')
@secure()
param value string

resource keyVault 'Microsoft.KeyVault/vaults@2024-04-01-preview' existing = {
  name: keyVaultName

  resource keyVaultSecret 'secrets' = {
    name: name
    properties: {
      value: value
      attributes: {
        enabled: true
      }
    }
  }
}

@description('ID for the deployed Key Vault Secret resource.')
output id string = keyVault::keyVaultSecret.id
@description('Name for the deployed Key Vault Secret resource.')
output name string = keyVault::keyVaultSecret.name
@description('URI for the deployed Key Vault Secret resource.')
output uri string = keyVault::keyVaultSecret.properties.secretUri
