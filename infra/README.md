# Infrastructure

This directory contains the infrastructure-as-code (IaC) templates and deployment scripts for provisioning and managing Azure resources using [Bicep](https://learn.microsoft.com/en-gb/azure/azure-resource-manager/bicep/overview?tabs=bicep).

## Table of Contents

- [Prerequisites](#prerequisites)
- [Folder Structure](#folder-structure)
- [Deployment](#deployment)
- [Teardown](#teardown)

## Prerequisites

- [Azure CLI](https://learn.microsoft.com/en-gb/cli/azure/install-azure-cli)
- [Azure Bicep tools](https://learn.microsoft.com/en-gb/azure/azure-resource-manager/bicep/install)
- Azure Subscription - You must have permission to create and manage resources in a target Azure subscription.

> [!NOTE]
> The necessary CLI tools should be installed by default in the devcontainer environment.

You can confirm Bicep is installed by running the following command:

```bash
az bicep version
```

## Folder Structure

```css
infra/
├── bicep/
│   ├── modules/
│   │   └── ...
│   ├── main.bicep
│   ├── main.bicepparam
│   └── ...
├── scripts/
│   ├── Deploy-Infrastructure.ps1
│   ├── deploy.sh
│   └── ...
└── README.md
```

- **bicep/**: Contains the Bicep templates and parameter files for provisioning Azure resources.
  - **modules/**: Contains reusable Bicep modules for creating resources.
- **scripts/**: Contains the deployment scripts for managing the resources, supporting both PowerShell and Bash.

## Deployment

> [!IMPORTANT]
> Although not required, the deployment can be configured to your specific needs by modifying the parameters in the [./bicep/main.bicepparam](./bicep/main.bicepparam) file. All parameters are optional, and if not provided, resources will be deployed using the naming conventions defined in the Azure Cloud Adoption Framework.

<details>
  <summary><strong>Expand to see the parameters</strong></summary>

> [!NOTE]
> For resource names that are marked as _Optional_, if not provided, the deployment will use the naming conventions defined in the Azure Cloud Adoption Framework. This means that the resource names will be automatically generated based on the `workloadName` and `location` parameters.

| Bicep Parameter              | Description                                                                                                                                |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| **workloadName**             | Name of the Azure environment to deploy.                                                                                                   |
| **location**                 | Azure region to deploy the resources, e.g. eastus2.                                                                                        |
| tags                         | _Optional_, Object containing the tags that will be assigned to all resources deployed resources.                                          |
| keyVaultName                 | _Optional_, Name of the Key Vault to use for storing secrets.                                                                              |
| logAnalyticsWorkspaceName    | _Optional_, Name of the Log Analytics Workspace to use for monitoring and logging.                                                         |
| applicationInsightsName      | _Optional_, Name of the Application Insights resource to use for monitoring.                                                               |
| aiServicesName               | _Optional_, Name of the Azure AI Services resource to use for deploying the Azure OpenAI chat completion model.                            |
| storageAccountName           | _Optional_, Name of the Azure Storage Account to use for storing data.                                                                     |
| aiFoundryHubName             | _Optional_, Name of the Azure AI Foundry Hub to use for managing the AI project.                                                           |
| aiFoundryProjectName         | _Optional_, Name of the Azure AI Foundry Project to use for managing the AI resources for the experiment.                                  |
| identities                   | _Optional_, Object containing the identities to assign least-privileged access Azure RBAC role assignments to.                             |
| raiPolicies                  | _Optional_, Object containing the Azure AI Content Safety policies to apply to deployed model endpoints in the Azure AI Services resource. |
| chatModelDeployment          | _Optional_, Object containing the details for the Azure OpenAI chat completion model deployment to use, e.g. gpt-4.1.                      |
| textEmbeddingModelDeployment | _Optional_, Object containing the details for the Azure OpenAI text embedding model deployment to use, e.g. text-embedding-3-large.        |
| phiModelDeployment           | _Optional_, Object containing the details for the Azure AI Phi model deployment to use, e.g. Phi-4.                                        |

</details>

To deploy the resources, run the following commands:

```bash
az login

./scripts/deploy.sh <deploymentName> <resourceGroupName> <location>
```

> [!NOTE]
> If a specific Azure tenant is required, use the `--tenant <TenantId>` parameter in the `az login` command.
> `az login --tenant <TenantId>`

> [!TIP]
> If you want to preview the changes without deployment, you can add the `--what-if` parameter.
> `./scripts/deploy.sh <deploymentName> <resourceGroupName> <location> --what-if`

This script will compile the Bicep templates and deploy the resources to the target Azure subscription.

## Teardown

To teardown the resources, run the following commands:

```bash
./scripts/teardown.sh <resourceGroupName>
```

This script will remove all resources provisioned by the deployment script.
