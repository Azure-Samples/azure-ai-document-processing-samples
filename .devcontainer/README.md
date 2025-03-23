# Azure AI Document Processing Samples - devcontainer

This devcontainer provides a development environment for running the samples in this repository. It includes all of the necessary tools and dependencies to setup and run every sample provided.

> [!NOTE]
> If there are any issues with the devcontainer, please open an issue in the repository.

## Base Image

The devcontainer is based on the `mcr.microsoft.com/devcontainers/base:1-bookworm` image. Additional tools and dependencies are installed on top of this base image.

## Features

The following container features are included in the devcontainer:

- **Git** - To provide version control.
- **PowerShell Core** - To run deployment scripts for the necessary infrastructure.
- **Azure CLI** - To managed the Azure resources.
- **Azure Developer CLI** - To manage the Azure resources.
- **.NET 9.0 & .NET 8.0 SDKs** - To run .NET samples.
- **Python 3.12** - To run Python samples.
- **GitHub CLI** - To interact with the GitHub repository.
- **Docker-in-Docker** - To run Docker containers from within the devcontainer.

## VS Code Extensions

The following VS Code extensions are included in the devcontainer:

### General

- **PowerShell** - To provide PowerShell language support.
- **Remote Development** - To enable support for Windows Subsystem for Linux (WSL) and devcontainers.
- **Prettier** - To format code.
- **IntelliCode** - To provide AI-assisted IntelliSense.
- **GitLens** - To improve Git repository information.
- **EditorConfig** - To provide EditorConfig support.

### GitHub

- **GitHub Repositories** - To browse, search, edit, and commit to GitHub repositories.
- **GitHub Copilot** - To provide AI-powered code completions and chat.
- **GitHub Pull Requests** - To review and manage GitHub pull requests.
- **GitHub Actions** - To manage GitHub actions.

### Azure

- **Azure Tools** - To provide Azure resource management support.
- **Azure Developer CLI** - To make it easier to run and create Azure resources with the Azure Developer CLI.
- **Bicep** - To provide Bicep language support.
- **Docker** - To make it easier to run Docker containers.
- **Azure Resources** - To view and manage Azure resources from within VS Code.
- **Azure Storage** - To view and manage Azure Storage resources from within VS Code.
- **GitHub Copilot for Azure** - To provide extensibility to GitHub Copilot to support with Azure related tasks.

### .NET

- **C# Dev Kit** - To provide C# language support.
- **Polyglot Notebooks** - To provide support for .NET interactive notebooks.

### Python

- **Python** - To provide Python language support.
- **Pylance** - To provide the default Python language server.
- **autopep8** - To support formatting Python code.
- **Python Debugger** - To debug Python code.
- **Jupyter** - To enable Jupyter notebook support.

## Linux Dependencies

The following Linux dependencies are included in the devcontainer:

- **poppler-utils** - To manipulate PDF files using the `pdf2image` and `pdf2image-dotnet` libraries.

## Python Dependencies

The following Python dependencies are included in the devcontainer:

- **azure-ai-documentintelligence** - To interact with the Azure AI Document Intelligence service.
- **azure-core** - To interact with the Azure services.
- **azure-identity** - To authenticate with the Azure services.
- **azure-ai-inference** - To interact with open models (e.g. Microsoft Phi) deployed to Azure AI Foundry.
- **azure-storage-blob** - To interact with the Azure Blob Storage service.
- **ipycanvas** - To create interactive canvases in Jupyter notebooks.
- **ipykernel** - To create Jupyter kernels.
- **matplotlib** - To create plots in Jupyter notebooks.
- **notebook** - To create Jupyter notebooks.
- **numpy** - To work with numerical data.
- **openai** - To interact with the Azure OpenAI service.
- **opencv-python** - To work with images.
- **openpyxl** - To work with Excel files.
- **pandas** - To work with data.
- **pdf2image** - To convert PDF files to images.
- **pydantic** - To work with data models.
- **pytesseract** - To extract text from images.
- **python-dotenv** - To load environment variables from a `.env` file.
- **seaborn** - To create plots in Jupyter notebooks.
- **tabulate** - To create tables in Jupyter notebooks.
- **tiktoken** - To calculate confidence scores for structured outputs using OpenAI's logprobs.

## .NET Dependencies

The following .NET dependencies are included in the samples:

- **Azure.AI.DocumentIntelligence** - To interact with the Azure AI Document Intelligence service.
- **Azure.AI.Inference** - To interact with open models (e.g. Microsoft Phi) deployed to Azure AI Foundry.
- **Azure.AI.OpenAI** - To interact with the Azure OpenAI service.
- **Azure.Identity** - To authenticate with the Azure services.
- **Azure.Storage.Blobs** - To interact with the Azure Blob Storage service.
- **DotNetEnv** - To load environment variables from a `.env` file.
- **Microsoft.ML.Tokenizers** and **Microsoft.ML.Tokenizers.Data.O200kBase** - To calculate confidence scores for structured outputs using OpenAI's logprobs.
- **pdf2image-dotnet** - To convert PDF files to images.
- **SkiaSharp** and **SkiaSharp.NativeAssets.Linux** - To render and manipulate images.
- **System.Numerics.Tensors** - To perform cosine similarity calculations for text vector embeddings.
