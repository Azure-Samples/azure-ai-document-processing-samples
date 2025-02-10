class AppSettings:
    """
    A class representing the configuration settings for the application.

    Attributes:
        resource_group_name: The name of the resource group.
        managed_identity_client_id: The client ID of the managed identity.
        storage_account_name: The name of the storage account.
        ai_services_endpoint: The endpoint for the AI services.
        openai_endpoint: The endpoint for the OpenAI service.
        gpt4o_model_deployment_name: The name of the GPT-4o model deployment.
        gpt4o_mini_model_deployment_name: The name of the GPT-4o Mini model deployment.
        text_embedding_model_deployment_name: The name of the text embedding model deployment.
        phi_endpoint: The endpoint for the Phi deployment.
        phi_primary_key: The primary key for the Phi deployment.
    """

    def __init__(self, config: dict):
        """
        Initializes a new instance of the AppSettings class.

        Args:
            config (dict): The environment configuration settings.        
        """

        self.resource_group_name = config['RESOURCE_GROUP_NAME']
        self.managed_identity_client_id = config['MANAGED_IDENTITY_CLIENT_ID']
        self.storage_account_name = config['STORAGE_ACCOUNT_NAME']
        self.ai_services_endpoint = config['AI_SERVICES_ENDPOINT']
        self.openai_endpoint = config['OPENAI_ENDPOINT']
        self.gpt4o_model_deployment_name = config['GPT4O_MODEL_DEPLOYMENT_NAME']
        self.gpt4o_mini_model_deployment_name = config['GPT4O_MINI_MODEL_DEPLOYMENT_NAME']
        self.text_embedding_model_deployment_name = config['TEXT_EMBEDDING_MODEL_DEPLOYMENT_NAME']
        self.phi_endpoint = config['PHI_ENDPOINT']
        self.phi_primary_key = config['PHI_PRIMARY_KEY']
