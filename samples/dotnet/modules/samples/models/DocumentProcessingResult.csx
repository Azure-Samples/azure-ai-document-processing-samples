using System.Collections.Generic;

public class DataProcessingResult<T>(
    T? data,
    Dictionary<string, object>? accuracy,
    Dictionary<string, object>? confidence,
    int? promptTokens,
    int? completionTokens,
    TimeSpan? executionTime)
{
    public T? Data { get; } = data;

    public Dictionary<string, object>? Accuracy { get; } = accuracy;

    public Dictionary<string, object>? Confidence { get; } = confidence;

    public int? PromptTokens { get; } = promptTokens;

    public int? CompletionTokens { get; } = completionTokens;

    public TimeSpan? ExecutionTime { get; } = executionTime;
}
