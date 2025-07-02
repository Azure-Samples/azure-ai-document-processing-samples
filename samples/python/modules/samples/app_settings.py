class AppSettings:
    """
    A class representing the configuration settings for the application.

    Attributes:
        azure_resource_group: The name of the resource group.
        azure_storage_account_name: The name of the storage account.
        azure_ai_services_endpoint: The endpoint for the AI services.
        azure_openai_endpoint: The endpoint for the OpenAI service.
        azure_openai_chat_deployment: The name of the GPT-4o model deployment.
        azure_openai_text_embedding_deployment: The name of the text embedding model deployment.
        azure_ai_phi_endpoint: The endpoint for the Phi deployment.
        azure_ai_phi_primary_key: The primary key for the Phi deployment.
    """

    def __init__(self, config: dict):
        """
        Initializes a new instance of the AppSettings class.

        Args:
            config (dict): The environment configuration settings.
        """

        self.azure_resource_group = config['AZURE_RESOURCE_GROUP']
        self.azure_storage_account_name = config['AZURE_STORAGE_ACCOUNT_NAME']
        self.azure_ai_services_endpoint = config['AZURE_AI_SERVICES_ENDPOINT']
        self.azure_openai_endpoint = config['AZURE_OPENAI_ENDPOINT']
        self.azure_openai_chat_deployment = config['AZURE_OPENAI_CHAT_DEPLOYMENT']
        self.azure_openai_text_embedding_deployment = config['AZURE_OPENAI_TEXT_EMBEDDING_DEPLOYMENT']
        self.azure_openai_api_version = config['AZURE_OPENAI_API_VERSION']
        self.azure_ai_phi_endpoint = config['AZURE_AI_PHI_ENDPOINT']
        self.azure_ai_phi_primary_key = config['AZURE_AI_PHI_PRIMARY_KEY']
