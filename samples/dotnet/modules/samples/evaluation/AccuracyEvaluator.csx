using System.Text.Json;

/// <summary>
/// A class for evaluating the accuracy of the comparison between two objects.
/// </summary>
public class AccuracyEvaluator<T>
{
    private readonly List<string> matchKeys;
    private readonly List<string> ignoreKeys;

    private int totalMatches;
    private int totalComparisons;

    /// <summary>
    /// Initializes a new instance of the AccuracyEvaluator class.
    /// </summary>
    /// <param name="matchKeys">The list of keys to use for matching objects in a list.</param>
    /// <param name="ignoreKeys">The list of keys to ignore during comparison.</param>
    public AccuracyEvaluator(List<string>? matchKeys = null, List<string>? ignoreKeys = null)
    {
        this.matchKeys = matchKeys ?? [];
        this.ignoreKeys = ignoreKeys ?? [];
        this.totalMatches = 0;
        this.totalComparisons = 0;
    }

    /// <summary>
    /// Evaluates the accuracy of the comparison between two objects.
    /// </summary>
    /// <param name="expected">The expected object as a JsonDocument.</param>
    /// <param name="actual">The actual object as a JsonDocument.</param>
    /// <returns>A dictionary with 'accuracy' and 'overall' keys, representing the accuracy structure and overall accuracy.</returns>
    public Dictionary<string, object> Evaluate(T? expected, T? actual)
    {
        // Convert objects to JsonDocuments.
        var expectedDoc = expected is null
            ? JsonDocument.Parse("{}")
            : JsonDocument.Parse(JsonSerializer.Serialize(expected));
        var actualDoc = actual is null
            ? JsonDocument.Parse("{}")
            : JsonDocument.Parse(JsonSerializer.Serialize(actual));

        // Reset counters for each evaluation.
        totalMatches = 0;
        totalComparisons = 0;

        // Compare root elements.
        var accuracy = CompareObjects(expectedDoc.RootElement, actualDoc.RootElement);

        // Compute overall accuracy.
        var overallAccuracy = (totalComparisons == 0)
            ? 1.0 // If nothing to compare, treat as accurate.
            : (double)totalMatches / totalComparisons;

        return new Dictionary<string, object> { { "accuracy", accuracy }, { "overall", overallAccuracy } };
    }

    private object CompareObjects(JsonElement expected, JsonElement actual)
    {
        switch (expected.ValueKind)
        {
            case JsonValueKind.Object:
                var resultDict = new Dictionary<string, object>();
                foreach (var prop in expected.EnumerateObject())
                {
                    // Skip ignored keys.
                    if (ignoreKeys.Contains(prop.Name))
                        continue;

                    var expVal = prop.Value;
                    JsonElement actVal = default;

                    // If actual is an object, try to find matching property.
                    if (actual.ValueKind == JsonValueKind.Object && actual.TryGetProperty(prop.Name, out var found))
                    {
                        actVal = found;
                    }

                    resultDict[prop.Name] = CompareObjects(expVal, actVal);
                }

                return resultDict;

            case JsonValueKind.Array:
                var accuracyList = new List<object>();
                var expectedList = expected.EnumerateArray().ToList();

                // If actual isn't array, all expected items mismatch.
                if (actual.ValueKind != JsonValueKind.Array)
                {
                    totalComparisons += expectedList.Count;
                    for (var i = 0; i < expectedList.Count; i++)
                        accuracyList.Add(0);
                    return accuracyList;
                }

                var actualList = actual.EnumerateArray().ToList();
                var usedIndices = new HashSet<int>();

                foreach (var expItem in expectedList)
                {
                    var matchFound = false;
                    object matchedAccuracy = 0;

                    // Attempt keyed matching if item is an object.
                    if (matchKeys.Count > 0 && expItem.ValueKind == JsonValueKind.Object)
                    {
                        foreach (var key in matchKeys)
                        {
                            if (!expItem.TryGetProperty(key, out var expKeyVal))
                                continue;

                            // Search for a matching actual item based on the key.
                            for (var idx = 0; idx < actualList.Count; idx++)
                            {
                                if (usedIndices.Contains(idx))
                                    continue;

                                var actItem = actualList[idx];
                                if (actItem.ValueKind != JsonValueKind.Object)
                                    continue;

                                if (!actItem.TryGetProperty(key, out var actKeyVal))
                                    continue;

                                // For strings, do case-insensitive compare.
                                bool keyMatch;
                                if (expKeyVal.ValueKind == JsonValueKind.String &&
                                    actKeyVal.ValueKind == JsonValueKind.String)
                                {
                                    keyMatch = expKeyVal.GetString().Equals(actKeyVal.GetString(),
                                        StringComparison.OrdinalIgnoreCase);
                                }
                                else
                                {
                                    keyMatch = ComparePrimitiveValues(expKeyVal, actKeyVal) == 1;
                                }

                                if (keyMatch)
                                {
                                    matchedAccuracy = CompareObjects(expItem, actItem);
                                    usedIndices.Add(idx);
                                    matchFound = true;
                                    break;
                                }
                            }

                            if (matchFound) break;
                        }
                    }

                    // If no keyed match found, attempt general matching.
                    if (!matchFound)
                    {
                        for (var idx = 0; idx < actualList.Count; idx++)
                        {
                            if (usedIndices.Contains(idx))
                                continue;

                            var actItem = actualList[idx];
                            matchedAccuracy = CompareObjects(expItem, actItem);

                            if (matchedAccuracy is 1)
                            {
                                usedIndices.Add(idx);
                                matchFound = true;
                                break;
                            }

                            if (matchedAccuracy is Dictionary<string, object> dictVal && IsFullyMatched(dictVal))
                            {
                                usedIndices.Add(idx);
                                matchFound = true;
                                break;
                            }

                            if (matchedAccuracy is List<object> listVal && IsFullyMatched(listVal))
                            {
                                usedIndices.Add(idx);
                                matchFound = true;
                                break;
                            }
                        }
                    }

                    // If match found, account for it.
                    if (matchFound)
                    {
                        if (matchedAccuracy is int primitiveAcc)
                        {
                            accuracyList.Add(primitiveAcc);
                            if (primitiveAcc == 1)
                                totalMatches++;

                            totalComparisons++;
                        }
                        else
                        {
                            // matchedAccuracy is dict or list.
                            accuracyList.Add(matchedAccuracy);
                            var (m, c) = CountMatches(matchedAccuracy);
                            totalMatches += m;
                            totalComparisons += c;
                        }
                    }
                    else
                    {
                        // No matching item found.
                        accuracyList.Add(0);
                        totalComparisons++;
                    }
                }

                return accuracyList;

            case JsonValueKind.Null:
            case JsonValueKind.Undefined:
                // Compare if both are null/undefined.
                totalComparisons++;
                if (actual.ValueKind is not (JsonValueKind.Null or JsonValueKind.Undefined))
                {
                    if (actual.ValueKind is not JsonValueKind.String || !string.IsNullOrEmpty(actual.GetString()))
                    {
                        return 0;
                    }

                    // Assume that a null or empty string is valid.
                    totalMatches++;
                    return 1;
                }

                totalMatches++;
                return 1;

            case JsonValueKind.String:
            case JsonValueKind.Number:
            case JsonValueKind.True:
            case JsonValueKind.False:
                // Compare primitive values.
                return ComparePrimitiveValues(expected, actual);

            default:
                // Catch-all.
                return 0;
        }
    }

    private int ComparePrimitiveValues(JsonElement expected, JsonElement actual)
    {
        totalComparisons++;

        switch (expected.ValueKind)
        {
            // If both are null or undefined.
            case JsonValueKind.Null or JsonValueKind.Undefined
                when actual.ValueKind is JsonValueKind.Null or JsonValueKind.Undefined:
                totalMatches++;
                return 1;
            // Case-insensitive string comparison.
            case JsonValueKind.String when actual.ValueKind == JsonValueKind.String:
                {
                    if (!expected.GetString().Equals(actual.GetString(), StringComparison.OrdinalIgnoreCase))
                    {
                        return 0;
                    }

                    totalMatches++;
                    return 1;
                }
        }

        // For other primitives.
        if (expected.ValueKind != actual.ValueKind)
        {
            return 0;
        }

        switch (expected.ValueKind)
        {
            case JsonValueKind.Number:
                if (expected.GetDouble() == actual.GetDouble())
                {
                    totalMatches++;
                    return 1;
                }

                break;
            case JsonValueKind.True:
            case JsonValueKind.False:
                if (expected.GetBoolean() == actual.GetBoolean())
                {
                    totalMatches++;
                    return 1;
                }

                break;
        }

        return 0;
    }

    private bool IsFullyMatched(Dictionary<string, object> dict)
    {
        return dict.Values.All(IsFullyMatched);
    }

    private bool IsFullyMatched(List<object> list)
    {
        return list.All(IsFullyMatched);
    }

    private bool IsFullyMatched(object val)
    {
        return val switch
        {
            int i => i == 1,
            Dictionary<string, object> dict => IsFullyMatched(dict),
            List<object> list => IsFullyMatched(list),
            _ => false
        };
    }

    private (int matches, int comparisons) CountMatches(object accuracy)
    {
        switch (accuracy)
        {
            case int i:
                return (i == 1 ? 1 : 0, 1);
            case Dictionary<string, object> dict:
                {
                    var m = 0;
                    var c = 0;
                    foreach (var v in dict.Values)
                    {
                        var (subM, subC) = CountMatches(v);
                        m += subM;
                        c += subC;
                    }

                    return (m, c);
                }
            case List<object> list:
                {
                    var m = 0;
                    var c = 0;
                    foreach (var item in list)
                    {
                        var (subM, subC) = CountMatches(item);
                        m += subM;
                        c += subC;
                    }

                    return (m, c);
                }
            default:
                return (0, 0);
        }
    }
}
