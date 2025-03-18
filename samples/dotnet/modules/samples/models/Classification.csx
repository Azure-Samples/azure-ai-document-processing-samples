public class ClassificationModel
{
    /// <summary>
    /// Gets or sets the page number of the classification.
    /// </summary>
    public int? PageNumber { get; set; }

    /// <summary>
    /// Gets or sets the classification of the page.
    /// </summary>
    public string? Classification { get; set; }

    /// <summary>
    /// Gets or sets the similarity of the classification from 0 to 100.
    /// </summary>
    public float? Similarity { get; set; }
}

public class ClassificationsModel
{
    /// <summary>
    /// Gets or sets the list of classifications.
    /// </summary>
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
}