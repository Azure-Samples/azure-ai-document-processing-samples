# Azure AI Document Processing Samples - devcontainer

This devcontainer provides a development environment for running the samples in this repository. It includes all of the necessary tools and dependencies to setup and run every sample provided.

> [!NOTE]
> If there are any issues with the devcontainer, please open an issue in the repository.

## Tools

The following tools are included in the devcontainer:

- **Git** - Used for version control.
- **PowerShell Core** - Used for running deployment scripts for the necessary infrastructure.
- **Azure CLI** - Used to managed the Azure resources.
- **Azure Developer CLI** - Used to manage the Azure resources.
- **Python 3.12** - Used for Python samples.
- **GitHub CLI** - Used to interact with the GitHub repository.
- **Docker-in-Docker** - Used to run Docker containers from within the devcontainer.

## VS Code Extensions

The following VS Code extensions are included in the devcontainer:

- **Python** - Python language support.
- **Pylance** - Python language server.
- **Python Debugger** - Python debugging support.
- **Jupyter** - Jupyter notebook support.
- **Bicep** - Bicep language support.
- **Azure Tools** - Azure resource management support.
- **PowerShell** - PowerShell language support.
- **GitHub Pull Requests** - GitHub pull request support.

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
