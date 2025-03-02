/// <summary>
/// Represents the configuration settings for the application.
/// </summary>
public class AppSettings
{
    public string ResourceGroupName { get; private set; }
    public string ManagedIdentityClientId { get; private set; }
    public string StorageAccountName { get; private set; }
    public string AIServicesEndpoint { get; private set; }
    public string OpenAIEndpoint { get; private set; }
    public string GPT4OModelDeploymentName { get; private set; }
    public string GPT4OMiniModelDeploymentName { get; private set; }
    public string TextEmbeddingModelDeploymentName { get; private set; }
    public string PhiEndpoint { get; private set; }
    public string PhiPrimaryKey { get; private set; }

    /// <summary>
    /// Initializes a new instance of the AppSettings class using the provided configuration.
    /// </summary>
    /// <param name="config">A dictionary containing the configuration settings.</param>
    public AppSettings(Dictionary<string, string> config)
    {
        if (config == null) throw new ArgumentNullException(nameof(config));

        ResourceGroupName = config["RESOURCE_GROUP_NAME"];
        ManagedIdentityClientId = config["MANAGED_IDENTITY_CLIENT_ID"];
        StorageAccountName = config["STORAGE_ACCOUNT_NAME"];
        AIServicesEndpoint = config["AI_SERVICES_ENDPOINT"];
        OpenAIEndpoint = config["OPENAI_ENDPOINT"];
        GPT4OModelDeploymentName = config["GPT4O_MODEL_DEPLOYMENT_NAME"];
        GPT4OMiniModelDeploymentName = config["GPT4O_MINI_MODEL_DEPLOYMENT_NAME"];
        TextEmbeddingModelDeploymentName = config["TEXT_EMBEDDING_MODEL_DEPLOYMENT_NAME"];
        PhiEndpoint = config["PHI_ENDPOINT"];
        PhiPrimaryKey = config["PHI_PRIMARY_KEY"];
    }
}