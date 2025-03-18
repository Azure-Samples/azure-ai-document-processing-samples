using System.Text.Json;
using Microsoft.ML.Tokenizers;
using OpenAI.Chat;

public static class OpenAIConfidence<T>
{
    /// <summary>
    /// Evaluate confidence for each field value in the extracted result based on the logprobs of the response from Azure OpenAI.
    /// </summary>
    /// <param name="result">The extracted result object.</param>
    /// <param name="choice">The choice object from the Azure OpenAI response.</param>
    /// <param name="model">The model name used for the response.</param>
    /// <returns>A dictionary with the confidence evaluations, including an "_overall" field for average confidence.</returns>
    public static Dictionary<string, object> EvaluateConfidence(
        T? result,
        ChatCompletion choice,
        string model = "gpt-4o")
    {
        var extractResult = result is null
            ? JsonDocument.Parse("{}")
            : JsonDocument.Parse(JsonSerializer.Serialize(result));

        var confidence = new Dictionary<string, object>();

        var encoding = TiktokenTokenizer.CreateForModel(model);

        // The original generated text from the response.
        var generatedText = choice.Content[0].Text;

        // Check if we have log probability information.
        var logProbInfo = choice.ContentTokenLogProbabilities;
        if (logProbInfo == null || logProbInfo.Count == 0)
        {
            confidence["_overall"] = 0.0;
            return confidence;
        }

        // Extract tokens and their log probabilities from the Azure OpenAI response.
        var tokens = logProbInfo.Select(x => x.Token).ToList();
        var tokenLogProbs = logProbInfo.Select(x => x.LogProbability).ToList();

        // Encode the entire generated text to map tokens to character positions
        var tokenOffsets = new List<(int Start, int End)>();
        var currentPos = 0;
        foreach (var tokenLength in from token in tokens
                                    select encoding.EncodeToTokens(token, out _)
                 into encodedToken
                                    select encoding.Decode(encodedToken.Select(x => x.Id))
                 into tokenStr
                                    select tokenStr.Length)
        {
            tokenOffsets.Add((currentPos, currentPos + tokenLength));
            currentPos += tokenLength;
        }

        // We'll advance substrOffset each time we match a field value.
        var substrOffset = 0;

        // Evaluate each top-level field in extractResult.
        foreach (var prop in extractResult.RootElement.EnumerateObject())
        {
            confidence[prop.Name] = EvaluateFieldValueConfidence(prop.Value);
        }

        // Compute overall average confidence.
        var confidenceValues = GetConfidenceValues(confidence);
        confidence["_overall"] = confidenceValues.Any() ? confidenceValues.Average() : 0.0;

        return confidence;

        // Recursively evaluate field values.
        object EvaluateFieldValueConfidence(JsonElement elem)
        {
            switch (elem.ValueKind)
            {
                case JsonValueKind.Object:
                    {
                        var dictResult = new Dictionary<string, object>();
                        foreach (var prop in elem.EnumerateObject())
                        {
                            dictResult[prop.Name] = EvaluateFieldValueConfidence(prop.Value);
                        }

                        return dictResult;
                    }
                case JsonValueKind.Array:
                    {
                        return elem.EnumerateArray().Select(EvaluateFieldValueConfidence).ToList();
                    }
                // For all primitive types (string, number, bool, null), evaluate confidence.
                default:
                    {
                        var valueStr = elem.ToString();

                        // Attempt to find this value in the generated text.
                        var startIndex = generatedText.IndexOf(valueStr, substrOffset, StringComparison.Ordinal);
                        if (startIndex < 0)
                        {
                            // If we can't find the text, return zero confidence.
                            return new Dictionary<string, object> { { "confidence", 0.0 }, { "value", valueStr } };
                        }

                        // Move our offset so subsequent searches start after this value.
                        substrOffset = startIndex + valueStr.Length;

                        // Identify which tokens overlap with this substring.
                        var tokenIndices = FindTokenIndices(valueStr, startIndex);
                        if (tokenIndices.Count == 0)
                        {
                            return new Dictionary<string, object> { { "confidence", 0.0 }, { "value", valueStr } };
                        }

                        // Collect the log probabilities of these tokens.
                        var valueLogProbs =
                            (from idx in tokenIndices where idx >= 0 && idx < tokenLogProbs.Count select tokenLogProbs[idx])
                            .Select(dummy => (double)dummy).ToList();

                        if (!valueLogProbs.Any())
                        {
                            return new Dictionary<string, object> { { "confidence", 0.0 }, { "value", valueStr } };
                        }

                        // Filter out extremely low logprobs (like -9999.0) to avoid skewing confidence.
                        var filteredLogProbs = valueLogProbs.Where(lp => lp > -9999.0).ToList();
                        if (!filteredLogProbs.Any())
                        {
                            return new Dictionary<string, object> { { "confidence", 0.0 }, { "value", valueStr } };
                        }

                        // Compute average log probability.
                        var avgLogProb = filteredLogProbs.Average();
                        // Convert to confidence.
                        var confVal = Math.Exp(avgLogProb);

                        // Clamp to [0, 1].
                        if (confVal < 0.0) confVal = 0.0;
                        if (confVal > 1.0) confVal = 1.0;

                        return new Dictionary<string, object> { { "confidence", confVal }, { "value", valueStr } };
                    }
            }
        }

        // Finds all token indices that overlap with the specified substring.
        List<int> FindTokenIndices(string substring, int startChar)
        {
            var endChar = startChar + substring.Length;
            var indices = new List<int>();
            for (var idx = 0; idx < tokenOffsets.Count; idx++)
            {
                var (start, end) = tokenOffsets[idx];
                // If token starts after substring ends, we can stop.
                if (start >= endChar)
                    break;

                // If token has any overlap with substring, include it.
                if (end > startChar)
                    indices.Add(idx);
            }

            return indices;
        }
    }

    /// <summary>
    /// Recursively extract confidence scores from any dictionary or list structure.
    /// </summary>
    private static List<double> GetConfidenceValues(object structure)
    {
        var values = new List<double>();

        switch (structure)
        {
            case Dictionary<string, object> dict:
                {
                    foreach (var kvp in dict)
                    {
                        if (kvp is { Key: "confidence", Value: double dblVal })
                        {
                            values.Add(dblVal);
                        }
                        else
                        {
                            values.AddRange(GetConfidenceValues(kvp.Value));
                        }
                    }

                    break;
                }
            case List<object> list:
                {
                    foreach (var item in list)
                    {
                        values.AddRange(GetConfidenceValues(item));
                    }

                    break;
                }
        }

        return values;
    }
}
