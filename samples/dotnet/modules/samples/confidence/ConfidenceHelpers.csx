public static class ConfidenceHelpers
{
    public static Dictionary<string, object> MergeConfidenceValues(
        Dictionary<string, object> confidenceA,
        Dictionary<string, object> confidenceB)
    {
        if (MergeFieldConfidenceValue(confidenceA, confidenceB) is not Dictionary<string, object> mergedConf)
            return confidenceA;

        var confidenceScores = GetConfidenceValues(mergedConf, "confidence");
        mergedConf["_overall"] = confidenceScores.Count > 0 ? confidenceScores.Average() : 0.0;
        return mergedConf;
    }

    public static List<double> GetConfidenceValues(Dictionary<string, object> data, string key = "confidence")
    {
        var confidenceValues = new List<double>();
        ExtractConfidenceValues(data, key, confidenceValues);
        return confidenceValues;
    }

    private static void ExtractConfidenceValues(object obj, string key, List<double> confidenceValues)
    {
        switch (obj)
        {
            case Dictionary<string, object> dict:
                foreach (var (k, v) in dict)
                {
                    if (k == key && TryGetConfidence(v, out var conf) && conf != 0)
                        confidenceValues.Add(conf);

                    if (v is Dictionary<string, object> or List<object>)
                        ExtractConfidenceValues(v, key, confidenceValues);
                }
                break;

            case List<object> list:
                foreach (var item in list)
                    ExtractConfidenceValues(item, key, confidenceValues);
                break;
        }
    }

    private static object? MergeFieldConfidenceValue(object fieldA, object fieldB)
    {
        switch (fieldA, fieldB)
        {
            case (Dictionary<string, object> dictA, Dictionary<string, object> dictB) when !dictA.ContainsKey("confidence"):
                var result = new Dictionary<string, object>();
                foreach (var (key, value) in dictA)
                {
                    if (key.StartsWith("_")) continue;
                    if (dictB.TryGetValue(key, out var bValue))
                    {
                        var merged = MergeFieldConfidenceValue(value, bValue);
                        if (merged != null) result[key] = merged;
                    }
                }
                return result;

            case (List<object> listA, List<object> listB) when listA.Count == listB.Count:
                var mergedList = new List<object>(listA.Count);
                for (var i = 0; i < listA.Count; i++)
                {
                    var merged = MergeFieldConfidenceValue(listA[i], listB[i]);
                    if (merged != null) mergedList.Add(merged);
                }
                return mergedList;

            case (Dictionary<string, object> aDict, Dictionary<string, object> bDict):
                double confA = GetConfidence(aDict), confB = GetConfidence(bDict);
                var mergedConfidence = (confA != 0 || confB != 0)
                    ? Math.Min(confA > 0 ? confA : double.MaxValue, confB > 0 ? confB : double.MaxValue)
                    : 0.0;

                var mergedValue = confA >= confB ? aDict["value"] : bDict["value"];
                return new Dictionary<string, object>
                {
                    { "confidence", mergedConfidence },
                    { "value", mergedValue }
                };

            default:
                return null;
        }
    }

    private static double GetConfidence(Dictionary<string, object> dict) =>
        dict.TryGetValue("confidence", out var value) && TryGetConfidence(value, out var confidence) ? confidence : 0.0;

    private static bool TryGetConfidence(object? value, out double confidence)
    {
        confidence = value switch
        {
            double d => d,
            string s when double.TryParse(s, out var parsed) => parsed,
            _ => 0.0
        };
        return confidence != 0;
    }
}
