@export()
@description('Connection information for the AI Hub/Project workspace.')
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

@description('Name of the AI Hub/Project workspace associated with the connection.')
param aiHubName string
@description('Connection information.')
param connection connectionInfo

resource hub 'Microsoft.MachineLearningServices/workspaces@2024-04-01-preview' existing = {
  name: aiHubName

  resource hubConnection 'connections@2024-01-01-preview' = {
    name: connection.name
    properties: {
      category: connection.category
      target: connection.target
      isSharedToAll: connection.isSharedToAll
      authType: connection.authType
      credentials: connection.credentials
      metadata: connection.metadata
    }
  }
}

@description('ID for the deployed AI Hub/Project workspace connection resource.')
output id string = hub::hubConnection.id
@description('Name for the deployed AI Hub/Project workspace connection resource.')
output name string = hub::hubConnection.name
