using System.ComponentModel;

public class ClassificationModel
{
    /// <summary>
    /// Gets or sets the page number of the classification.
    /// </summary>
    [Description("The page number of the classification.")]
    public int? PageNumber { get; set; }

    /// <summary>
    /// Gets or sets the classification of the page.
    /// </summary>
    [Description("The classification of the page.")]
    public string? Classification { get; set; }

    /// <summary>
    /// Gets or sets the similarity of the classification from 0 to 100.
    /// </summary>
    [Description("The similarity of the classification from 0 to 100.")]
    public float? Similarity { get; set; }
}

public class ClassificationsModel
{
    /// <summary>
    /// Gets or sets the list of classifications.
    /// </summary>
    [Description("The list of classifications.")]
    public List<ClassificationModel> Classifications { get; set; } = new();

    public ClassificationModel GetClassification(int pageNumber)
    {
        return Classifications.FirstOrDefault(c => c.PageNumber == pageNumber);
    }
}

public class ClassificationDefinitionModel
{
    public string Classification { get; set; }

    public string Description { get; set; }

    public List<string> Keywords { get; set; } = new();

    public float[]? Embedding { get; set; }
}
