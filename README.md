---
page_type: sample
languages:
  - python
  - csharp
  - bicep
products:
  - azure
  - ai-services
  - azure-openai
  - document-intelligence
  - language-service
  - azure-translator
name: Document Processing with Azure AI Samples
description: This collection of samples demonstrates how to use various Azure AI capabilities to build a solution to extract structured data, classify, redact, and analyze documents.
---

# Document Processing with Azure AI Samples

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Azure-Samples/azure-ai-document-processing-samples?quickstart=1)

This repository contains a collection of code samples that demonstrate how to use various Azure AI capabilities to process documents.

The samples are intended to help engineering teams establish techniques with Azure AI Foundry, Azure OpenAI, Azure AI Document Intelligence, and Azure AI Language services to build solutions to extract structured data, classify, and analyze documents.

The techniques demonstrated take advantage of various capabilities from each service to:

- **Reduce complexity of custom model training** by taking advantage of the capabilities of Generative AI models to analyze and classify documents.
- **Improve reliability in document processing** by utilizing combining AI service capbilities to extract structured data from any document type, with high accuracy and confidence.
- **Simplify document processing workflows** by providing reusable code and patterns that can be easily modified and evaluated for most use cases.

## Contents

- [Samples](#samples)
  - [Document Classification](#document-classification)
  - [Document Redaction](#document-redaction)
  - [Document Extraction](#document-extraction)
- [Use Case Scenarios](#use-case-scenarios)
- [Getting Started](#getting-started)
  - [Setup on GitHub Codespaces](#setup-on-github-codespaces)
  - [Setup on Local](#setup-on-local)
  - [Deploy the Azure environment](#deploy-the-azure-environment)
- [Contributing](#contributing)
- [License](#license)

## Samples

### Document Classification

| Sample                                                    | Link                                                                                                                                                                             | Description                                                                                                                           | Example Use Cases                                                                                                       |
| --------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| Vision-based Classification with Azure OpenAI GPT-4o      | [Python](./samples/python/classification/document-classification-gpt-vision.ipynb) \| [.NET](./samples/dotnet/classification/document-classification-gpt-vision.ipynb)           | Use Azure OpenAI GPT-4o models to classify documents using their built-in vision capabilities.                                        | Processing multiple documents types or documents with varying purposes, such as contracts, legal documents, and emails. |
| Semantic Similarity Classification with Vector Embeddings | [Python](./samples/python/classification/document-classification-text-embeddings.ipynb) \| [.NET](./samples/dotnet/classification/document-classification-text-embeddings.ipynb) | Use Azure OpenAI embedding models to convert document text and classify them based on similarity to pre-defined classification lists. | Processing multiple documents types or documents with varying purposes, such as contracts, legal documents, and emails. |

### Document Redaction

| Sample                                                                                              | Link                                                                                                                                                                           | Description                                                                                                                                                                                      | Example Use Cases                                                                                                                                                   |
| --------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| LLM-enabled Redaction with Azure AI Document Intelligence, Azure OpenAI GPT-4o, and Post-Processing | [Python](./samples/python/redaction/document-redaction-gpt.ipynb) \| [.NET](./samples/dotnet/redaction/document-redaction-gpt.ipynb)                                           | Use Azure AI Document Intelligence `prebuilt-layout` and Azure OpenAI GPT models to redact sensitive information from documents using natural language instruction to determine redaction areas. | Require specific redaction rules, such as redacting based on context or relationships. Also works for redacting PII, including names, addresses, and phone numbers. |
| Document Redaction with Azure AI Language PII Native Document Analysis                              | [Python](./samples/python/redaction/document-redaction-language-native-document.ipynb) \| [.NET](./samples/dotnet/redaction/document-redaction-language-native-document.ipynb) | Use Azure AI Language Native Document Analysis to redact personally identifiable information (PII) from documents.                                                                               | Redacting sensitive information from documents, such as names, addresses, and phone numbers.                                                                        |

### Document Extraction

> [!NOTE]
> All data extraction samples provide both an accuracy and confidence score for the extracted data. The accuracy score is calculated based on the similarity between the extracted data and the ground truth data. The confidence score can be calculated based on OCR analysis confidence and `logprobs` in Azure OpenAI responses.

| Sample                                                                                               | Link                                                                                                                                                                                           | Description                                                                                                                            | Example Use Cases                                                                                                                     |
| ---------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| Text-based Extraction with Azure AI Document Intelligence and Azure OpenAI GPT-4o                    | [Python](./samples/python/extraction/text/document-extraction-gpt.ipynb) \| [.NET](./samples/dotnet/extraction/text/document-extraction-gpt.ipynb)                                             | Use Azure AI Document Intelligence `prebuilt-layout` and Azure OpenAI GPT models to extract structured data from documents using text. | Predominantly text-based documents such as invoices, receipts, and forms.                                                             |
| Text-based Extraction with Azure AI Document Intelligence and Microsoft Phi                          | [Python](./samples/python/extraction/text/document-extraction-phi.ipynb) \| [.NET](./samples/dotnet/extraction/text/document-extraction-phi.ipynb)                                             | Use Azure AI Document Intelligence `prebuilt-layout` and Microsoft's Phi models to extract structured data from documents using text.  | Predominantly text-based documents such as invoices, receipts, and forms.                                                             |
| Vision-based Extraction with Azure OpenAI GPT-4o GPT-4o                                              | [Python](./samples/python/extraction/vision/document-extraction-gpt-vision.ipynb) \| [.NET](./samples/dotnet/extraction/vision/document-extraction-gpt-vision.ipynb)                           | Use Azure OpenAI GPT-4o models to extract structured data from documents using vision capabilities.                                    | Complex documents with a mix of text and images, including diagrams, signatures, selection marks, etc. such as reports and contracts. |
| Multi-Modal (Text and Vision) Extraction with Azure AI Document Intelligence and Azure OpenAI GPT-4o | [Python](./samples/python/extraction/multimodal/document-extraction-gpt-text-and-vision.ipynb) \| [.NET](./samples/dotnet/extraction/multimodal/document-extraction-gpt-text-and-vision.ipynb) | Improve the accuracy and confidence in extracting structured data from documents by combining text and images with LLMs.               | Any structured or unstructured document type.                                                                                         |

## Use Case Scenarios

This repo also contains a collection of end-to-end use case scenarios that demonstrate how to combine the various samples to create a real-world scenario for document processing.

| Scenario    | Link                                                                                                                                           | Description                                                                                                                                                                                                                                                                                                   |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Invoice** | [Python](./samples/python/scenarios/invoices/invoice-extraction.ipynb) \| [.NET](./samples/dotnet/scenarios/invoices/invoice-extraction.ipynb) | Using a structured Invoice object ([Python](./samples/python/modules/samples/models/invoice.py) \| [.NET](./samples/dotnet/modules/samples/models/Invoice.csx)), invoice documents can be extracted into a standard Invoice schema by first classifying which pages to extract from using boundary detection. |

## Getting Started

The sample repository comes with a [**Dev Container**](./.devcontainer/README.md) that contains all the necessary tools and dependencies to run the sample. Please review the [**container and it's dependencies**](./.devcontainer/README.md) to understand all of the necessary components required to run these in a real-world environment, including the use of [Poppler](https://poppler.freedesktop.org/).

> [!IMPORTANT]
> An Azure subscription is required to run these samples. If you don't have an Azure subscription, create an [account](https://azure.microsoft.com/en-us/).

### Setup on GitHub Codespaces

To use the Dev Container in GitHub Codespaces, follow these steps:

1. Click on the `Code` button in the repository and select `Codespaces`.
2. Click on the **+** button to create a new Codespace using the provided `.devcontainer\devcontainer.json` configuration.
3. Once the Codespace is created, continue to the [Azure environment setup](#deploy-the-azure-environment) section.

### Setup on Local

To use the Dev Container, you need to have the following tools installed on your local machine:

- Install [**Visual Studio Code**](https://code.visualstudio.com/download)
- Install [**Docker Desktop**](https://www.docker.com/products/docker-desktop)
- Install [**Remote - Containers**](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension for Visual Studio Code

To setup a local development environment, follow these steps:

> [!IMPORTANT]
> Ensure that Docker Desktop is running on your local machine.

1. Clone the repository to your local machine.
2. Open the repository in Visual Studio Code.
3. Press `F1` to open the command palette and type `Dev Containers: Reopen in Container`.

Once the Dev Container is up and running, continue to the [Azure environment setup](#deploy-the-azure-environment) section.

### Deploy the Azure environment

Once the Dev Container is up and running, you can setup the necessary Azure services and run the [samples](#samples) in the repository by running the following command in a `pwsh` terminal:

> [!NOTE]
> For the most optimal sample experience, it is recommended to run the samples in `East US` which will provide support for all the services used in the samples. Find out more about region availability for [Azure AI Document Intelligence](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/concept-layout?view=doc-intel-4.0.0&tabs=sample-code), and [`GPT-4o`](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models#standard-and-global-standard-deployment-model-quota), [`Phi-4`](https://azure.microsoft.com/en-us/pricing/details/phi-3/), and [`text-embedding-3-large`](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models#standard-deployment-model-availability) models.

```pwsh
az login

./Setup-Environment.ps1 -DeploymentName <UniqueDeploymentName> -Location <AzureRegion>
```

> [!NOTE]
> If a specific Azure tenant is required, use the `--tenant <TenantId>` parameter in the `az login` command.
> `az login --tenant <TenantId>`

> [!TIP]
> If you want to preview the changes without deployment, you can add the `-WhatIf` parameter to the `Setup-Environment.ps1` script.
> `./Setup-Environment.ps1 -DeploymentName <UniqueDeploymentName> -Location <AzureRegion> -WhatIf`

The script will deploy the following resources to your Azure subscription:

- [**Azure AI Foundry Hub & Project**](https://learn.microsoft.com/en-us/azure/ai-studio/what-is-ai-studio), a development platform for building AI solutions that integrates with Azure AI Services in a secure manner using Microsoft Entra ID for authentication.
  - **Note**: Phi-4 MoE will be deployed as a [PAYG serverless endpoint in the Azure AI Foundry Project](https://ai.azure.com/explore/models/Phi-4/version/3/registry/azureml) with its primary key stored in the associated Azure Key Vault.
- [**Azure AI Services**](https://learn.microsoft.com/en-us/azure/ai-services/what-are-ai-services), a managed service for all Azure AI Services, including Azure OpenAI, Azure AI Document Intelligence, and Azure AI Language services.
  - **Note**: GPT-4o and GPT-4o-mini will be deployed as Global Standard models with 10K TPM quota allocation. `text-embedding-3-large` will be deployed as a Standard model with 115K TPM quota allocation. These can be adjusted based on your quota availability in the [main.bicep](./infra/main.bicep) file.
- [**Azure Storage Account**](https://learn.microsoft.com/en-us/azure/storage/common/storage-introduction), required by Azure AI Foundry.
- [**Azure Monitor**](https://learn.microsoft.com/en-us/azure/azure-monitor/overview), used to store logs and traces for monitoring and troubleshooting purposes.
- [**Azure Container Registry**](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-intro), used to store container images for the Azure AI Foundry environment.

> [!NOTE]
> All resources are secured by default with Microsoft Entra ID using Azure RBAC. Your user client ID will be added with the necessary least-privilege roles to access the resources created. A user-assigned managed identity will also be deployed for the Azure AI Foundry environment.

After the script completes, you can run any of the samples in the repository by following their instructions.

## Contributing

You can contribute to the repository by opening an issue or submitting a pull request. For more information, see the [Contributing](./CONTRIBUTING.md) guide.

## License

This project is licensed under the [MIT License](./LICENSE).
