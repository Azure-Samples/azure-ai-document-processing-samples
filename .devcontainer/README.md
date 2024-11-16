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
- **.NET 8.0 SDK** - Used for .NET samples.
- **Node 22.x** - Used for JavaScript samples.
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
- **C# Dev Kit** - C# language support.
- **GitHub Pull Requests** - GitHub pull request support.
- **Polyglot Notebooks** - Jupyter notebook support for C# and PowerShell.

## Python Dependencies

The following Python dependencies are included in the devcontainer:

- **azure-ai-documentintelligence** - To interact with the Azure AI Document Intelligence service.
- **azure-core** - To interact with the Azure services.
- **azure-identity** - To authenticate with the Azure services.
- **azure-storage-blob** - To interact with the Azure Blob Storage service.
- **ipycanvas** - To create interactive canvases in Jupyter notebooks.
- **ipykernel** - To create Jupyter kernels.
- **marker-pdf** - To extract text from PDF files as Markdown.
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
- **surya-ocr** - To extract text from images.
- **tiktoken** - To calculate confidence scores for structured outputs using OpenAI's logprobs.
- **transformers** - To interact with the Hugging Face Transformers library.
