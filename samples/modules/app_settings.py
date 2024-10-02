class AppSettings:
    def __init__(self, config: dict):
        self.resource_group_name = config['RESOURCE_GROUP_NAME']
        self.managed_identity_client_id = config['MANAGED_IDENTITY_CLIENT_ID']
        self.storage_account_name = config['STORAGE_ACCOUNT_NAME']
        self.ai_services_endpoint = config['AI_SERVICES_ENDPOINT']
        self.openai_endpoint = config['OPENAI_ENDPOINT']
        self.gpt4o_model_deployment_name = config['GPT4O_MODEL_DEPLOYMENT_NAME']
        self.text_embedding_model_deployment_name = config['TEXT_EMBEDDING_MODEL_DEPLOYMENT_NAME']
        self.phi35_mini_endpoint = config['PHI35_MINI_ENDPOINT']
        self.phi35_mini_primary_key = config['PHI35_MINI_PRIMARY_KEY']
