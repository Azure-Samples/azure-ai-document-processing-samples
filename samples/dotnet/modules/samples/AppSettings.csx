/// <summary>
/// Represents the configuration settings for the application.
/// </summary>
public class AppSettings
{
    public string AzureResourceGroup { get; private set; }
    public string AzureStorageAccountName { get; private set; }
    public string AzureAIServicesEndpoint { get; private set; }
    public string AzureOpenAIEndpoint { get; private set; }
    public string AzureOpenAIChatDeployment { get; private set; }
    public string AzureOpenAITextEmbeddingDeployment { get; private set; }
    public string AzureOpenAIApiVersion { get; private set; }
    public string AzureAIPhiEndpoint { get; private set; }
    public string AzureAIPhiPrimaryKey { get; private set; }

    /// <summary>
    /// Initializes a new instance of the AppSettings class using the provided configuration.
    /// </summary>
    /// <param name="config">A dictionary containing the configuration settings.</param>
    public AppSettings(Dictionary<string, string> config)
    {
        ArgumentNullException.ThrowIfNull(config);

        AzureResourceGroup = config["AZURE_RESOURCE_GROUP"];
        AzureStorageAccountName = config["AZURE_STORAGE_ACCOUNT_NAME"];
        AzureAIServicesEndpoint = config["AZURE_AI_SERVICES_ENDPOINT"];
        AzureOpenAIEndpoint = config["AZURE_OPENAI_ENDPOINT"];
        AzureOpenAIChatDeployment = config["AZURE_OPENAI_CHAT_DEPLOYMENT"];
        AzureOpenAITextEmbeddingDeployment = config["AZURE_OPENAI_TEXT_EMBEDDING_DEPLOYMENT"];
        AzureOpenAIApiVersion = config["AZURE_OPENAI_API_VERSION"];
        AzureAIPhiEndpoint = config["AZURE_AI_PHI_ENDPOINT"];
        AzureAIPhiPrimaryKey = config["AZURE_AI_PHI_PRIMARY_KEY"];
    }
}
