using System.Collections.Generic;

public class DataClassificationResult<T>(T? classification, Dictionary<string, object>? accuracy, TimeSpan? executionTime)
{
    public T? Classification { get; } = classification;

    public Dictionary<string, object>? Accuracy { get; } = accuracy;

    public TimeSpan? ExecutionTime { get; } = executionTime;
}
