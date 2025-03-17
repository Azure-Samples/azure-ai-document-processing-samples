using System.Collections.Generic;

public class DataClassificationResult<T>(T? classification, Dictionary<string, object>? accuracy)
{
    public T? Classification { get; } = classification;

    public Dictionary<string, object>? Accuracy { get; } = accuracy;
}
