using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using Azure.Core;
using Azure.Core.Pipeline;

public class LanguageNativePIIClient
{
    private const string DefaultAuthorizationScope = "https://cognitiveservices.azure.com/.default";
    private readonly Uri _endpoint;
    private readonly HttpPipeline _pipeline;
    private readonly string _apiVersion;
    private readonly TokenCredential _credential;

    public LanguageNativePIIClient(Uri endpoint, TokenCredential credential)
    {
        ArgumentNullException.ThrowIfNull(endpoint, nameof(endpoint));
        ArgumentNullException.ThrowIfNull(credential, nameof(credential));

        _credential = credential;
        _pipeline = HttpPipelineBuilder.Build(new HttpPipelineOptions(ClientOptions.Default)
        {
            PerRetryPolicies = { new BearerTokenAuthenticationPolicy(credential, DefaultAuthorizationScope) }
        });
        _endpoint = endpoint;
        _apiVersion = "2024-11-15-preview";
    }

    public virtual async Task<AnalyzeNativePIIResult> AnalyzeDocumentAsync(
        AnalyzeNativePIIOptions options,
        CancellationToken cancellationToken = default)
    {
        var accessToken = await _credential.GetTokenAsync(new TokenRequestContext([DefaultAuthorizationScope]), cancellationToken);

        var requestContent = JsonSerializer.Serialize(options, JsonSerializerOptions.Web);

        var request = _pipeline.CreateRequest();
        request.Content = RequestContent.Create(Encoding.UTF8.GetBytes(requestContent));
        request.Method = RequestMethod.Post;
        request.Uri.Reset(_endpoint);
        request.Uri.AppendPath("/language", escape: false);
        request.Uri.AppendPath("/analyze-documents/", escape: false);
        request.Uri.AppendPath("jobs", escape: false);
        request.Uri.AppendQuery("api-version", _apiVersion, true);
        request.Headers.Add("Authorization", new AuthenticationHeaderValue("Bearer", accessToken.Token).ToString());
        request.Headers.Add("Accept", "application/json");
        request.Headers.Add("Content-Type", "application/json");

        var response = await _pipeline.SendRequestAsync(request, cancellationToken);

        if (response.Status == 202)
        {
            response.Headers.TryGetValue("Operation-Location", out var operationLocation);

            if (operationLocation != null)
            {
                var operationUri = new Uri(operationLocation);

                while (true)
                {
                    var operationRequest = _pipeline.CreateRequest();
                    operationRequest.Method = RequestMethod.Get;
                    operationRequest.Uri.Reset(operationUri);
                    var operationResponse = await _pipeline.SendRequestAsync(operationRequest, cancellationToken);
                    if (operationResponse.Status == 200)
                    {
                        var operationContent = operationResponse.Content.ToString();
                        var result = JsonSerializer.Deserialize<AnalyzeNativePIIResult>(operationContent, JsonSerializerOptions.Web);
                        if (result != null)
                        {
                            if (result.Errors != null && result.Errors.Any())
                            {
                                throw new InvalidOperationException(JsonSerializer.Serialize(result.Errors, JsonSerializerOptions.Web));
                            }

                            var taskErrors = result.Tasks.Items.SelectMany(x => x.Results.Errors);
                            if (taskErrors.Any())
                            {
                                throw new InvalidOperationException(JsonSerializer.Serialize(taskErrors, JsonSerializerOptions.Web));
                            }

                            if (result.Status == "succeeded")
                            {
                                return result;
                            }
                        }
                        else
                        {
                            throw new InvalidOperationException("No result returned.");
                        }
                    }

                    await Task.Delay(1000, cancellationToken);
                }
            }
        }

        throw new InvalidOperationException($"Unexpected response: {response.Status}. {response.Content}");
    }
}

public class AnalyzeNativePIIResult
{
    public string JobId { get; set; }

    public DateTime LastUpdatedDateTime { get; set; }

    public DateTime CreatedDateTime { get; set; }

    public DateTime ExpirationDateTime { get; set; }

    public string Status { get; set; }

    public IEnumerable<AnalyzeNativePIIResultError>? Errors { get; set; }

    public string DisplayName { get; set; }

    public AnalyzeNativePIIResultTasks Tasks { get; set; }
}

public class AnalyzeNativePIIResultTasks
{
    public int Completed { get; set; }

    public int Failed { get; set; }

    public int InProgress { get; set; }

    public int Total { get; set; }

    public IEnumerable<AnalyzeNativePIIResultTask> Items { get; set; }
}

public class AnalyzeNativePIIResultTask
{
    public string Kind { get; set; }

    public string TaskName { get; set; }

    public DateTime LastUpdateDateTime { get; set; }

    public string Status { get; set; }

    public AnalyzeNativePIIResultTaskResult Results { get; set; }
}

public class AnalyzeNativePIIResultTaskResult
{
    public IEnumerable<AnalyzeNativePIIResultDocument> Documents { get; set; }

    public IEnumerable<AnalyzeNativePIIResultError>? Errors { get; set; }

    public string ModelVersion { get; set; }
}

public class AnalyzeNativePIIResultDocument
{
    public string Id { get; set; }

    public AnalyzeNativePIIResultDocumentLocation Source { get; set; }

    public IEnumerable<AnalyzeNativePIIResultDocumentLocation> Targets { get; set; }

    public IEnumerable<string>? Warnings { get; set; }
}

public class AnalyzeNativePIIResultDocumentLocation
{
    public string Kind { get; set; }

    public string Location { get; set; }
}

public class AnalyzeNativePIIResultError
{
    public string Id { get; set; }

    public Dictionary<string, object> Error { get; set; }
}

public class AnalyzeNativePIIOptions(string displayName, AnalyzeInputOptions analysisInput, IEnumerable<AnalyzeNativePIIInputTask> tasks)
{
    public string DisplayName { get; set; } = displayName;

    public AnalyzeInputOptions AnalysisInput { get; set; } = analysisInput;

    public IEnumerable<AnalyzeNativePIIInputTask> Tasks { get; set; } = tasks;
}

public class AnalyzeNativePIIInputTask(string taskName, AnalyzeInputTaskParameters parameters)
{
    public string Kind => "PiiEntityRecognition";

    public string TaskName { get; set; } = taskName;

    public AnalyzeInputTaskParameters Parameters { get; set; } = parameters;
}

public class AnalyzeInputTaskParameters(AnalyzeInputTaskRedactionPolicy redactionPolicy, IEnumerable<string> piiCategories, bool excludeExtractionData)
{
    public AnalyzeInputTaskRedactionPolicy RedactionPolicy { get; set; } = redactionPolicy;

    public IEnumerable<string> PiiCategories { get; set; } = piiCategories;

    public bool ExcludeExtractionData { get; set; } = excludeExtractionData;
}

public class AnalyzeInputTaskRedactionPolicy(string policyKind = AnalyzeInputTaskRedactionPolicy.CharacterMask)
{
    public const string NoMask = "noMask";
    public const string CharacterMask = "characterMask";
    public const string EntityMask = "entityMask";

    public string PolicyKind { get; set; } = CharacterMask;
}

public class AnalyzeInputOptions(IEnumerable<AnalyzeInputDocument> documents)
{
    public IEnumerable<AnalyzeInputDocument> Documents { get; set; } = documents;
}

public class AnalyzeInputDocument(string id, AnalyzeInputDocumentLocation source, AnalyzeInputDocumentLocation target, string language = "en")
{
    public string Language { get; set; } = language;

    public string Id { get; set; } = id;

    public AnalyzeInputDocumentLocation Source { get; set; } = source;

    public AnalyzeInputDocumentLocation Target { get; set; } = target;
}

public class AnalyzeInputDocumentLocation(string location)
{
    public string Location { get; set; } = location;
}
