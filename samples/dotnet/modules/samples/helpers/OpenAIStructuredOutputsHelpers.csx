using System.ClientModel;
using System.Text.Json;
using System.Text.Json.Nodes;
using System.Text.Json.Schema;
using System.Text.Json.Serialization;
using System.Threading;
using System.Threading.Tasks;
using OpenAI.Chat;

public class ParsedChatCompletion<T>
{
    internal ParsedChatCompletion(ChatCompletion completion)
    {
        Origin = completion;

        Id = completion.Id;
        Model = completion.Model;
        SystemFingerprint = completion.SystemFingerprint;
        Usage = completion.Usage;
        CreatedAt = completion.CreatedAt;
        FinishReason = completion.FinishReason;
        ContentTokenLogProbabilities = completion.ContentTokenLogProbabilities;
        RefusalTokenLogProbabilities = completion.RefusalTokenLogProbabilities;
        Role = completion.Role;
        Content = completion.Content;
        ToolCalls = completion.ToolCalls;
        Refusal = completion.Refusal;
        Parsed = JsonSerializer.Deserialize<T?>(completion.Content[0].Text);
    }

    [JsonIgnore] public ChatCompletion Origin { get; }

    public string Id { get; }

    public string Model { get; }

    public string SystemFingerprint { get; }

    public ChatTokenUsage Usage { get; }

    public DateTimeOffset CreatedAt { get; }

    public ChatFinishReason FinishReason { get; }

    public IReadOnlyList<ChatTokenLogProbabilityDetails> ContentTokenLogProbabilities { get; }

    public IReadOnlyList<ChatTokenLogProbabilityDetails> RefusalTokenLogProbabilities { get; }

    public ChatMessageRole Role { get; }

    public ChatMessageContent Content { get; }

    public IReadOnlyList<ChatToolCall> ToolCalls { get; }

    public string Refusal { get; }

    public T? Parsed { get; }

    public static implicit operator ParsedChatCompletion<T?>(ChatCompletion result)
    {
        return new ParsedChatCompletion<T?>(result);
    }

    public static implicit operator ParsedChatCompletion<T?>(ClientResult<ChatCompletion> result)
    {
        return new ParsedChatCompletion<T?>(result);
    }
}

public static Func<JsonSchemaExporterContext, JsonNode, JsonNode> StructuredOutputsTransform = (_, node) =>
{
    if (node is JsonObject rootObject)
    {
        ProcessJsonObject(rootObject);
    }

    return node;

    static void ProcessJsonObject(JsonObject jsonObject)
    {
        if (jsonObject["type"]?.ToString().Contains("object") != true)
        {
            return;
        }

        // Ensures that object types include the "additionalProperties" field, set to false.
        if (!jsonObject.ContainsKey("additionalProperties"))
        {
            jsonObject.Add("additionalProperties", false);
        }

        var required = new JsonArray();
        var properties = jsonObject["properties"] as JsonObject;
        foreach (var property in properties!)
        {
            required.Add(property.Key);
            if (property.Value is JsonObject nestedObject)
            {
                // Process nested objects to ensure schema validity.
                ProcessJsonObject(nestedObject);
            }
        }

        // Ensures that object types include the "required" field containing all the property keys.
        if (!jsonObject.ContainsKey("required"))
        {
            jsonObject.Add("required", required);
        }
    }
};

public static ParsedChatCompletion<T?> CompleteChat<T>(
    this ChatClient chatClient,
    List<ChatMessage> messages,
    ChatCompletionOptions? options = null,
    CancellationToken cancellationToken = default)
{
    return chatClient.CompleteChat(messages, options, cancellationToken);
}

public static async Task<ParsedChatCompletion<T?>> CompleteChatAsync<T>(
    this ChatClient chatClient,
    List<ChatMessage> messages,
    ChatCompletionOptions? options = null,
    CancellationToken cancellationToken = default)
{
    return await chatClient.CompleteChatAsync(messages, options, cancellationToken);
}

public static ChatResponseFormat CreateJsonSchemaFormat<T>(
    string jsonSchemaFormatName,
    string? jsonSchemaFormatDescription = null,
    bool? jsonSchemaIsStrict = null)
{
    return ChatResponseFormat.CreateJsonSchemaFormat(
        jsonSchemaFormatName,
        jsonSchema: BinaryData.FromString(JsonSerializerOptions.Default.GetJsonSchemaAsNode(typeof(T),
            new JsonSchemaExporterOptions()
            {
                TreatNullObliviousAsNonNullable = true,
                TransformSchemaNode = StructuredOutputsTransform
            }).ToString()),
        jsonSchemaFormatDescription: jsonSchemaFormatDescription,
        jsonSchemaIsStrict: jsonSchemaIsStrict
    );
}
