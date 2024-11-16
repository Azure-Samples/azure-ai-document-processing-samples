---
page_type: sample
languages:
- python
- bicep
products:
- azure
- ai-services
- azure-openai
name: Document Processing with Azure AI Samples
description: This collection of samples demonstrates how to use various Azure AI capabilities to build solution to extract structured data, classify, and analyze documents.
---

# Document Processing with Azure AI Samples

This repository contains a collection of code samples that demonstrate how to use various Azure AI capabilities to process documents.

The samples are intended to help engineering teams establish techniques with Azure AI Studio, Azure OpenAI, and Azure Document Intelligence to build solutions to extract structured data, classify, and analyze documents.

The techniques demonstrated take advance of various capabilities from each service to:

- **Reduce complexity of custom model training** by taking advantage of the capabilities of Generative AI models to analyze and classify documents.
- **Improve reliability in document processing** by utilizing combining AI service capbilities to extract structured data from any document type, with high accuracy and confidence.
- **Simplify document processing workflows** by providing reusable code and patterns that can be easily modified and evaluated for most use cases.

## Contents

- [Samples](#samples)
- [Getting Started](#getting-started)
- [Contributing](#contributing)
- [License](#license)

## Samples

> [!NOTE]
> All data extraction samples provide both an accuracy and confidence score for the extracted data. The accuracy score is calculated based on the similarity between the extracted data and the ground truth data. The confidence score is calculated based on OCR analysis confidence and `logprobs` in Azure OpenAI requests.

| Sample                                                                                             | Description                                                                                                                                    | Example Use Cases                                                         |
| -------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| [Data Extraction - Azure AI Document Intelligence + Azure OpenAI GPT-4o](./samples/extraction/text-based/document-intelligence-openai.ipynb) | Demonstrates how to use Azure AI Document Intelligence pre-built layout and Azure OpenAI GPT models to extract structured data from documents. | Predominantly text-based documents such as invoices, receipts, and forms. |
| [Data Extraction - Azure AI Document Intelligence + Phi-3.5 MoE](./samples/extraction/text-based/document-intelligence-phi.ipynb) | Demonstrates how to use Azure AI Document Intelligence pre-built layout and Microsoft's Phi-3 models to extract structured data from documents. | Predominantly text-based documents such as invoices, receipts, and forms. |
| [Data Extraction - Marker/Surya + Azure OpenAI GPT-4o](./samples/extraction/text-based/marker-surya-openai.ipynb) | Demonstrates how to use Marker/Surya and Azure OpenAI GPT models to extract structured data from documents. | Predominantly text-based documents such as invoices, receipts, and forms. |
| [Data Extraction - Azure OpenAI GPT-4o with Vision](./samples/extraction/vision-based/openai.ipynb) | Demonstrates how to use Azure OpenAI GPT-4o and GPT-4o-mini models to extract structured data from documents using their built-in vision capabilities. | Complex documents with a mix of text and images, including diagrams, signatures, selection marks, etc. such as reports and contracts. |
| [Data Extraction - Comprehensive Azure AI Document Intelligence + Azure OpenAI GPT-4o with Vision](./samples/extraction/vision-based/comprehensive.ipynb) | Demonstrates how to improve the accuracy and confidence in extracting structured data from documents by combining Azure AI Document Intelligence and Azure OpenAI GPT-4o models with vision capabilities. | Any structured or unstructured document type. |
| [Classification - Azure OpenAI GPT-4o with Vision](./samples/classification/openai.ipynb) | Demonstrates how to use Azure OpenAI GPT-4o and GPT-4o-mini models to classify documents using their built-in vision capabilities. | Processing multiple documents types or documents with varying purposes, such as contracts, legal documents, and emails. |
| [Classification - Azure AI Document Intelligence + Embeddings](./samples/classification/document-intelligence-embeddings.ipynb) | Demonstrates how to use Azure AI Document Intelligence pre-built layout and embeddings models to classify documents based on their content. | Processing multiple documents types or documents with varying purposes, such as contracts, legal documents, and emails. |

## Getting Started

The sample repository comes with a [**Dev Container**](./.devcontainer/README.md) that contains all the necessary tools and dependencies to run the sample. To use the Dev Container, you need to have the following tools installed on your local machine:

- Install [**Visual Studio Code**](https://code.visualstudio.com/download)
- Install [**Docker Desktop**](https://www.docker.com/products/docker-desktop)
- Install [**Remote - Containers**](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension for Visual Studio Code

Additionally, you will require:

- An Azure subscription. If you don't have an Azure subscription, create an [account](https://azure.microsoft.com/en-us/).

To setup a local development environment, follow these steps:

> [!NOTE]
> Ensure that Docker Desktop is running on your local machine.

1. Clone the repository to your local machine.
2. Open the repository in Visual Studio Code.
3. Press `F1` to open the command palette and type `Dev Containers: Reopen in Container`.

Once the Dev Container is up and running, you can setup the necessary Azure services and run the [samples](#samples) in the repository by running the following command in VS Code's `pwsh` terminal:

> [!NOTE]
> For the most optimal sample experience, it is recommended to run the samples in `East US` which will provide support for all the services used in the samples. Find out more about region availability for [Azure AI Document Intelligence](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/concept-layout?view=doc-intel-4.0.0&tabs=sample-code), and [`GPT-4o`](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models#standard-and-global-standard-deployment-model-quota), [`Phi-3.5 MoE`](https://azure.microsoft.com/en-us/pricing/details/phi-3/), and [`text-embedding-3-large`](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models#standard-deployment-model-availability) models.

```pwsh
az login

./Setup-Environment.ps1 -DeploymentName <UniqueDeploymentName> -Location <AzureRegion> -SkipInfrastructure $false
```

The script will deploy the following resources to your Azure subscription:

- [**Azure AI Studio Hub & Project**](https://learn.microsoft.com/en-us/azure/ai-studio/what-is-ai-studio), a development platform for building AI solutions that integrates with Azure AI Services in a secure manner using Microsoft Entra ID for authentication.
  - **Note**: Phi-3.5 MoE will be deployed as a [PAYG serverless endpoint in the Azure AI Studio Project](https://ai.azure.com/explore/models/Phi-3.5-MoE-instruct/version/4/registry/azureml?tid=ffd04b18-2c0c-4078-82eb-4d8558089235) with its primary key stored in the associated Azure Key Vault.
- [**Azure AI Services**](https://learn.microsoft.com/en-us/azure/ai-services/what-are-ai-services), a managed service for all Azure AI Services, including Azure OpenAI and Azure AI Document Intelligence.
  - **Note**: GPT-4o and GPT-4o-mini will be deployed as Global Standard models with 10K TPM quota allocation. `text-embedding-3-large` will be deployed as a Standard model with 115K TPM quota allocation. These can be adjusted based on your quota availability in the [main.bicep](./infra/main.bicep) file.
- [**Azure Storage Account**](https://learn.microsoft.com/en-us/azure/storage/common/storage-introduction), required by Azure AI Studio.
- [**Azure Monitor**](https://learn.microsoft.com/en-us/azure/azure-monitor/overview), used to store logs and traces for monitoring and troubleshooting purposes.
- [**Azure Container Registry**](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-intro), used to store container images for the Azure AI Studio environment.

> [!NOTE]
> All resources are secured by default with Microsoft Entra ID using Azure RBAC. Your user client ID will be added with the necessary least-privilege roles to access the resources created. A user-assigned managed identity will also be deployed for the Azure AI Studio environment.

After the script completes, you can run any of the samples in the repository by following their instructions.

## Contributing

You can contribute to the repository by opening an issue or submitting a pull request. For more information, see the [Contributing](./CONTRIBUTING.md) guide.

## License

This project is licensed under the [MIT License](./LICENSE).
