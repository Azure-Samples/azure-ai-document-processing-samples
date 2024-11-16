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
        text_embedding_model_deployment_name: The name of the text embedding model deployment.
        phi3_endpoint: The endpoint for the Phi-3 deployment.
        phi3_primary_key: The primary key for the Phi-3 deployment.
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
        self.text_embedding_model_deployment_name = config['TEXT_EMBEDDING_MODEL_DEPLOYMENT_NAME']
        self.phi3_endpoint = config['PHI3_ENDPOINT']
        self.phi3_primary_key = config['PHI3_PRIMARY_KEY']
