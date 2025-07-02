@description('Name of the AI Foundry Hub or Project associated with the connection.')
param aiFoundryName string
@description('Connection information.')
param connection connectionInfo

// Deployments

resource aiFoundry 'Microsoft.MachineLearningServices/workspaces@2025-01-01-preview' existing = {
  name: aiFoundryName

  resource hubConnection 'connections@2025-01-01-preview' = {
    name: connection.name
    properties: {
      category: connection.category
      target: connection.?target
      isSharedToAll: connection.?isSharedToAll
      authType: connection.?authType
      credentials: connection.?credentials
      metadata: connection.?metadata
    }
  }
}

// Outputs

@description('ID for the deployed AI Foundry Hub or Project connection resource.')
output id string = aiFoundry::hubConnection.id
@description('Name for the deployed AI Foundry Hub or Project connection resource.')
output name string = aiFoundry::hubConnection.name

// Definitions

@export()
@description('Connection information for the AI Foundry Hub or Project.')
type connectionInfo = {
  @description('Name of the connection.')
  name: string
  @description('Category of the connection.')
  category: string
  @description('Indicates whether the connection is shared to all projects.')
  isSharedToAll: bool
  @description('Target of the connection.')
  target: string?
  @description('Authentication type for the connection target.')
  authType:
    | 'AAD'
    | 'AccessKey'
    | 'AccountKey'
    | 'ApiKey'
    | 'CustomKeys'
    | 'ManagedIdentity'
    | 'None'
    | 'OAuth2'
    | 'PAT'
    | 'SAS'
    | 'ServicePrincipal'
    | 'UsernamePassword'
  @description('Credentials for the connection target.')
  credentials: object?
  @description('Metadata for the connection target.')
  metadata: object?
}
