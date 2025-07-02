using './main.bicep'

param workloadName = 'ai-document-data-extraction'
param location = 'eastus'
param tags = {
  WorkloadName: workloadName
  DataClassification: 'General'
  Criticality: 'Medium'
  Environment: 'Dev'
  RepositoryUrl: 'https://github.com/azure-samples/azure-ai-document-processing-samples'
}
param keyVaultName = ''
param logAnalyticsWorkspaceName = ''
param applicationInsightsName = ''
param aiServicesName = ''
param storageAccountName = ''
param aiFoundryHubName = ''
param aiFoundryProjectName = ''
param identities = []
param raiPolicies = [
  {
    name: workloadName
    mode: 'Blocking'
    prompt: {}
    completion: {}
  }
]
param chatModelDeployment = {
  name: 'gpt-4.1'
  model: { format: 'OpenAI', name: 'gpt-4.1', version: '2025-04-14' }
  sku: { name: 'GlobalStandard', capacity: 50 }
  raiPolicyName: workloadName
  versionUpgradeOption: 'OnceCurrentVersionExpired'
}
param textEmbeddingModelDeployment = {
  name: 'text-embedding-3-large'
  model: { format: 'OpenAI', name: 'text-embedding-3-large', version: '1' }
  sku: { name: 'Standard', capacity: 100 }
  raiPolicyName: workloadName
  versionUpgradeOption: 'OnceCurrentVersionExpired'
}
