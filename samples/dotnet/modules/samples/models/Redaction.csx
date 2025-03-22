using System.ComponentModel;

public class RedactionWord
{
    [Description("The bounding box of the word to redact. Example [0.5768, 0.5639, 1.8538, 0.564, 1.8538, 0.8636, 0.5759, 0.86].")]
    public List<float> Polygon { get; set; }

    [Description("The text content to redact.")]
    public string Content { get; set; }

    [Description("The category of the entity to redact, e.g. 'Name', 'Address', 'Phone Number'.")]
    public string Category { get; set; }
}

public class Redaction
{
    [Description("The page number of the document.")]
    public int PageNumber { get; set; }

    [Description("Optional - The words to redact from the document.")]
    public List<RedactionWord>? Words { get; set; }
}