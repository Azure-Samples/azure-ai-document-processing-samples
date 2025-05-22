using System.ComponentModel;

/// <summary>
/// A class representing a classification or a collection of page images from a document.
/// </summary>
[Description("A class representing a classification or a collection of page images from a document.")]
public class ClassificationModel
{
    /// <summary>
    /// Gets or sets the classification of the page.
    /// </summary>
    [Description("Classification of the page, e.g., invoice, receipt, etc.")]
    public string? Classification { get; set; }

    /// <summary>
    /// Gets or sets the start page number of the classification.
    /// </summary>
    [Description("If a single document associated with the classification spans multiple pages, this field specifies the start of the image range, e.g., 1.")]
    public int? ImageRangeStart { get; set; }

    /// <summary>
    /// Gets or sets the end page number of the classification.
    /// </summary>
    [Description("If a single document associated with the classification spans multiple pages, this field specifies the end of the image range, e.g., 20.")]
    public int? ImageRangeEnd { get; set; }
}

/// <summary>
/// A class representing a list of document page image classifications.
/// </summary>
[Description("A class representing a list of document page image classifications.")]
public class ClassificationsModel
{
    /// <summary>
    /// Gets or sets the list of document page image classifications.
    /// </summary>
    [Description("List of document page image classifications.")]
    public List<ClassificationModel> Classifications { get; set; } = new();
}

public class ClassificationDefinitionModel
{
    public string Classification { get; set; }

    public string Description { get; set; }

    public List<string> Keywords { get; set; } = new();

    public float[]? Embedding { get; set; }
}
