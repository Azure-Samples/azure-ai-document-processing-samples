using System.Text.Json;
using System.Text.Json.Serialization;
using Azure;
using Azure.AI.Inference;

public class ParsedChatCompletions<T>
{
    internal ParsedChatCompletions(ChatCompletions completion)
    {
        Origin = completion;

        Id = completion.Id;
        Created = completion.Created;
        Model = completion.Model;
        Usage = completion.Usage;
        Content = completion.Content;
        Role = completion.Role;
        FinishReason = completion.FinishReason;
        ToolCalls = completion.ToolCalls;

        var contentJson = Content;
        contentJson = contentJson.Replace("```json", "").Replace("```", "").Trim();

        Parsed = JsonSerializer.Deserialize<T?>(contentJson);
    }

    [JsonIgnore] public ChatCompletions Origin { get; }

    public string Id { get; }

    public DateTimeOffset Created { get; }

    public string Model { get; }

    public CompletionsUsage Usage { get; }

    public string Content { get; }

    public ChatRole Role { get; }

    public CompletionsFinishReason? FinishReason { get; }

    public IReadOnlyList<ChatCompletionsToolCall> ToolCalls { get; }

    public T? Parsed { get; }

    public static implicit operator ParsedChatCompletions<T?>(ChatCompletions result)
    {
        return new ParsedChatCompletions<T?>(result);
    }

    public static implicit operator ParsedChatCompletions<T?>(Response<ChatCompletions> result)
    {
        return new ParsedChatCompletions<T?>(result);
    }
}
