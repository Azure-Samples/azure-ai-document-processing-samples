using System.Text.Json;
using Azure.AI.DocumentIntelligence;

public static class DocumentIntelligenceConfidence<T>
{
    public static Dictionary<string, object> EvaluateConfidence(
        T? result,
        AnalyzeResult analysis)
    {
        var extractResult = result is null
            ? JsonDocument.Parse("{}")
            : JsonDocument.Parse(JsonSerializer.Serialize(result));

        var confidence = new Dictionary<string, object>();
        var confidenceScores = new List<float>();

        var lines = ExtractLines(analysis);

        foreach (var prop in extractResult.RootElement.EnumerateObject())
        {
            confidence[prop.Name] = EvaluateFieldValueConfidence(prop.Value);
        }

        confidence["_overall"] = confidenceScores.Average();

        return confidence;

        List<(List<DocumentWord> Words, float Confidence)> ExtractLines(AnalyzeResult a)
        {
            var l = new List<(List<DocumentWord> Words, float Confidence)>();

            foreach (var page in a.Pages)
            {
                foreach (var line in page.Lines)
                {
                    var lineWords = new List<DocumentWord>();
                    var lineConfidences = new List<float>();

                    foreach (var span in line.Spans)
                    {
                        var offsetStart = span.Offset;
                        var offsetEnd = span.Offset + span.Length;

                        lineWords.AddRange(page.Words.Where(w =>
                            w.Span.Offset >= offsetStart && w.Span.Offset + w.Span.Length <= offsetEnd));
                    }

                    lineConfidences = lineWords.Select(w => w.Confidence).ToList();

                    l.Add((lineWords, lineConfidences.Min()));
                }
            }

            return l;
        }

        object EvaluateFieldValueConfidence(JsonElement value)
        {
            switch (value.ValueKind)
            {
                case JsonValueKind.Object:
                    {
                        var c = new Dictionary<string, object>();
                        foreach (var prop in value.EnumerateObject())
                        {
                            c[prop.Name] = EvaluateFieldValueConfidence(prop.Value);
                        }

                        return c;
                    }
                case JsonValueKind.Array:
                    return value.EnumerateArray().Select(EvaluateFieldValueConfidence).ToList();
                default:
                    {
                        var c = new Dictionary<string, object>();
                        var matchingLines = FindMatchingLines(
                            value,
                            lines);

                        var fieldConfidenceScore = matchingLines.Select(x => x.Confidence).DefaultIfEmpty(0).Min();

                        confidenceScores.Add(fieldConfidenceScore);

                        c["confidence"] = fieldConfidenceScore;
                        c["lines"] = matchingLines;
                        c["value"] = value.ToString();

                        return c;
                    }
            }
        }

        List<(List<DocumentWord> Words, float Confidence)> FindMatchingLines(JsonElement value,
            List<(List<DocumentWord> Words, float Confidence)> l)
        {
            var valueStrs = value.ToString().Split(" ", StringSplitOptions.RemoveEmptyEntries);

            var matchingLines = l.Where(line =>
                valueStrs.Any(val =>
                    line.Words.Any(w => w.Content.Equals(val, StringComparison.OrdinalIgnoreCase)))
            ).ToList();

            if (!matchingLines.Any())
            {
                matchingLines = l.Where(line =>
                    valueStrs.Any(val =>
                        line.Words.Any(w => w.Content.Contains(val, StringComparison.OrdinalIgnoreCase)))
                ).ToList();
            }

            return matchingLines;
        }
    }
}
