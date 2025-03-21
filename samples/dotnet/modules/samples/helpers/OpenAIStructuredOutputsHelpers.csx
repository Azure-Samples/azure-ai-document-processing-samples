using System.ClientModel;
using System.Collections;
using System.ComponentModel;
using System.Reflection;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Threading;
using System.Threading.Tasks;
using OpenAI;
using OpenAI.Chat;

/// <summary>
/// A utility class to generate JSON Schema compatible with OpenAI's Structured Outputs subset.
/// </summary>
public static class OpenAIJsonSchema
{
    /// <summary>
    /// Generates a JSON Schema (as a string) compatible with OpenAI's Structured Outputs subset for the specified generic type.
    /// </summary>
    public static string For<T>() => For(typeof(T));

    /// <summary>
    /// Generates a JSON Schema (as a string) compatible with OpenAI's Structured Outputs subset for the specified <see cref="Type"/>.
    /// </summary>
    public static string For(Type t)
    {
        var visited = new HashSet<Type>();
        var definitions = new Dictionary<string, object>();

        // Build the top-level object schema
        var rootSchema = BuildRootObjectSchema(t, visited, definitions);

        // If we have child definitions, add them to the root
        if (definitions.Count > 0)
        {
            rootSchema["$defs"] = definitions;
        }

        // Serialize
        return JsonSerializer.Serialize(rootSchema, new JsonSerializerOptions { WriteIndented = true });
    }

    /// <summary>
    /// Builds the top-level schema for an object, adding references and definitions for sub-objects.
    /// </summary>
    private static Dictionary<string, object> BuildRootObjectSchema(
        Type t,
        HashSet<Type> visited,
        Dictionary<string, object> definitions)
    {
        // Treat the root as a standard object schema with type="object", properties=..., required=..., additionalProperties=false
        var (properties, required) = BuildPropertiesForType(t, visited, definitions);

        return new Dictionary<string, object>
        {
            ["type"] = "object",
            ["properties"] = properties,
            ["required"] = required,
            ["additionalProperties"] = false
        };
    }

    /// <summary>
    /// Builds the property definitions and "required" list for a given type.
    /// </summary>
    private static (Dictionary<string, object> properties, List<string> required) BuildPropertiesForType(
        Type t,
        HashSet<Type> visited,
        Dictionary<string, object> definitions)
    {
        var propsDict = new Dictionary<string, object>();
        var requiredList = new List<string>();

        // Only consider public instance properties
        var props = t.GetProperties(BindingFlags.Public | BindingFlags.Instance);
        foreach (var prop in props)
        {
            requiredList.Add(prop.Name);

            // Build the JSON Schema for this property
            var propertySchema = BuildPropertySchema(
                prop.PropertyType,
                visited,
                definitions);

            var description = GetDescription(prop.GetCustomAttributes());
            if (!string.IsNullOrEmpty(description))
            {
                propertySchema["description"] = description;
            }

            propsDict[prop.Name] = propertySchema;
        }

        return (propsDict, requiredList);
    }

    /// <summary>
    /// Decides how to represent the schema for a property type.
    /// </summary>
    /// <remarks>
    /// Handles:
    /// 1) Primitives (string, bool, numeric, enum)
    /// 2) Nullable primitives/enums => anyOf [T, null]
    /// 3) Arrays or Lists => { type="array", items=... }
    /// 4) Complex objects => $ref to a definition, possibly with anyOf if it's a reference type
    /// </remarks>
    private static Dictionary<string, object> BuildPropertySchema(
        Type propType,
        HashSet<Type> visited,
        Dictionary<string, object> definitions)
    {
        if (IsNullableValueType(propType))
        {
            var underlying = Nullable.GetUnderlyingType(propType);
            var baseSchema = BuildSingleTypeSchema(underlying, visited, definitions);
            return new Dictionary<string, object>
            {
                ["anyOf"] = new List<object> { baseSchema, new Dictionary<string, object> { ["type"] = "null" } }
            };
        }

        if (propType.IsValueType || propType == typeof(string))
        {
            // If it's a non-nullable primitive or enum or string
            return BuildSingleTypeSchema(propType, visited, definitions);
        }

        // If it's some kind of enumerable (array/list) => array schema
        if (typeof(IEnumerable).IsAssignableFrom(propType) && propType != typeof(string))
        {
            var arrSchema = BuildArraySchema(propType, visited, definitions);
            return new Dictionary<string, object>
            {
                ["anyOf"] = new List<object> { arrSchema, new Dictionary<string, object> { ["type"] = "null" } }
            };
        }

        // Otherwise, it's a complex object => $ref
        var refSchema = BuildComplexObjectRef(propType, visited, definitions);
        return new Dictionary<string, object>
        {
            ["anyOf"] = new List<object> { refSchema, new Dictionary<string, object> { ["type"] = "null" } }
        };
    }

    private static bool IsNullableValueType(Type t)
    {
        return t.IsGenericType && t.GetGenericTypeDefinition() == typeof(Nullable<>);
    }

    /// <summary>
    /// Builds the schema for a single type that is not wrapped by anyOf (no nulls here). This includes non-nullable primitives, enums, or reference strings.
    /// </summary>
    private static Dictionary<string, object> BuildSingleTypeSchema(Type t, HashSet<Type> visited, Dictionary<string, object> definitions)
    {
        // Enums => { "type": "string", "enum": [ ... ] }
        if (t.IsEnum)
        {
            return new Dictionary<string, object>
            {
                ["type"] = "string",
                ["enum"] = Enum.GetNames(t)
            };
        }

        // Strings
        if (t == typeof(string) || t == typeof(char) || t == typeof(DateTime))
        {
            return new Dictionary<string, object>
            {
                ["type"] = "string"
            };
        }

        // Boolean
        if (t == typeof(bool))
        {
            return new Dictionary<string, object>
            {
                ["type"] = "boolean"
            };
        }

        // Numeric
        switch (Type.GetTypeCode(t))
        {
            case TypeCode.Byte:
            case TypeCode.Int16:
            case TypeCode.Int32:
            case TypeCode.Int64:
            case TypeCode.SByte:
            case TypeCode.UInt16:
            case TypeCode.UInt32:
            case TypeCode.UInt64:
                return new Dictionary<string, object>
                {
                    ["type"] = "integer"
                };

            case TypeCode.Single:
            case TypeCode.Double:
            case TypeCode.Decimal:
                return new Dictionary<string, object>
                {
                    ["type"] = "number"
                };
        }

        // If it's an object/struct that's not an enum, we treat it as a complex object
        return t is { IsValueType: true, IsPrimitive: false } ?
            // Treat as an object, which might contain properties.
            BuildComplexObjectRef(t, visited, definitions) :
            // Fallback to string
            new Dictionary<string, object>
            {
                ["type"] = "string"
            };
    }

    /// <summary>
    /// Builds an array schema for the given collection type.
    /// </summary>
    private static Dictionary<string, object> BuildArraySchema(Type t, HashSet<Type> visited, Dictionary<string, object> definitions)
    {
        // If it's an array, element type is t.GetElementType()
        // If it's a generic IEnumerable/List, element type is t.GetGenericArguments()[0]
        // Otherwise fallback to object
        Type? elementType = null;

        if (t.IsArray)
        {
            elementType = t.GetElementType();
        }
        else if (t.IsGenericType)
        {
            elementType = t.GetGenericArguments().FirstOrDefault();
        }

        elementType ??= typeof(object);

        var itemSchema = BuildPropertySchema(elementType, visited, definitions);

        return new Dictionary<string, object> { ["type"] = "array", ["items"] = itemSchema };
    }

    /// <summary>
    /// Builds or reuses a definition for a complex object type, returning a $ref.
    /// </summary>
    private static Dictionary<string, object> BuildComplexObjectRef(Type t, HashSet<Type> visited, Dictionary<string, object> definitions)
    {
        var key = GetDefinitionKey(t);

        // If we've already built a definition for this type, just return a ref.
        if (definitions.ContainsKey(key))
        {
            return new Dictionary<string, object>
            {
                ["$ref"] = $"#/$defs/{key}"
            };
        }

        // If we've visited this type but not built a definition, it means it's self-referencing.
        // Creates an empty placeholder definition, so any references to this type will simply use the $ref instead of building it again.
        if (!visited.Add(t))
        {
            // Create a placeholder definition if none is added
            definitions[key] = new Dictionary<string, object>
            {
                ["type"] = "object",
                ["properties"] = new Dictionary<string, object>(),
                ["required"] = new List<string>(),
                ["additionalProperties"] = false
            };

            return new Dictionary<string, object> { ["$ref"] = $"#/$defs/{key}" };
        }

        // Build and add an empty definition up front so that if we come across t again while building, we don't end up infinitely recursing.
        definitions[key] = new Dictionary<string, object>
        {
            ["type"] = "object",
            ["properties"] = new Dictionary<string, object>(),
            ["required"] = new List<string>(),
            ["additionalProperties"] = false
        };

        // Fill out the properties.
        var (props, req) = BuildPropertiesForType(t, visited, definitions);

        // Update the existing placeholder in definitions
        (definitions[key] as Dictionary<string, object>)["properties"] = props;
        (definitions[key] as Dictionary<string, object>)["required"] = req;

        // Return the reference
        return new Dictionary<string, object>
        {
            ["$ref"] = $"#/$defs/{key}"
        };
    }

    /// <summary>
    /// Retrieves the DescriptionAttribute for a type, or falls back to the type's name.
    /// </summary>
    private static string GetDescription(IEnumerable<Attribute> attributes)
    {
        var descAttr = attributes
            .OfType<DescriptionAttribute>()
            .FirstOrDefault();

        return descAttr?.Description ?? string.Empty;
    }

    /// <summary>
    /// Produces a name to store in the $defs dictionary.
    /// </summary>
    private static string GetDefinitionKey(Type t)
    {
        return t.Name;
    }
}

public class ParsedChatCompletion<T>
{
    internal ParsedChatCompletion(ChatCompletion completion)
    {
        Origin = completion;

        Id = completion.Id;
        Model = completion.Model;
        SystemFingerprint = completion.SystemFingerprint;
        Usage = completion.Usage;
        CreatedAt = completion.CreatedAt;
        FinishReason = completion.FinishReason;
        ContentTokenLogProbabilities = completion.ContentTokenLogProbabilities;
        RefusalTokenLogProbabilities = completion.RefusalTokenLogProbabilities;
        Role = completion.Role;
        Content = completion.Content;
        ToolCalls = completion.ToolCalls;
        Refusal = completion.Refusal;
        Parsed = JsonSerializer.Deserialize<T?>(completion.Content[0].Text);
    }

    [JsonIgnore] public ChatCompletion Origin { get; }

    public string Id { get; }

    public string Model { get; }

    public string SystemFingerprint { get; }

    public ChatTokenUsage Usage { get; }

    public DateTimeOffset CreatedAt { get; }

    public ChatFinishReason FinishReason { get; }

    public IReadOnlyList<ChatTokenLogProbabilityDetails> ContentTokenLogProbabilities { get; }

    public IReadOnlyList<ChatTokenLogProbabilityDetails> RefusalTokenLogProbabilities { get; }

    public ChatMessageRole Role { get; }

    public ChatMessageContent Content { get; }

    public IReadOnlyList<ChatToolCall> ToolCalls { get; }

    public string Refusal { get; }

    public T? Parsed { get; }

    public static implicit operator ParsedChatCompletion<T?>(ChatCompletion result)
    {
        return new ParsedChatCompletion<T?>(result);
    }

    public static implicit operator ParsedChatCompletion<T?>(ClientResult<ChatCompletion> result)
    {
        return new ParsedChatCompletion<T?>(result);
    }
}


public static ChatResponseFormat CreateJsonSchemaFormat<T>(
    string jsonSchemaFormatName,
    string? jsonSchemaFormatDescription = null,
    bool? jsonSchemaIsStrict = null)
{
    var formatObjectType = typeof(T);
    var type = formatObjectType.IsGenericType && formatObjectType.GetGenericTypeDefinition() == typeof(Nullable<>)
        ? Nullable.GetUnderlyingType(formatObjectType)!
        : formatObjectType;

    var jsonSchema = OpenAIJsonSchema.For(type);

    return ChatResponseFormat.CreateJsonSchemaFormat(
        jsonSchemaFormatName,
        jsonSchema: BinaryData.FromString(jsonSchema),
        jsonSchemaFormatDescription: jsonSchemaFormatDescription,
        jsonSchemaIsStrict: jsonSchemaIsStrict
    );
}

public static ParsedChatCompletion<T?> CompleteChat<T>(
    this ChatClient chatClient,
    List<ChatMessage> messages,
    ChatCompletionOptions? options = null,
    CancellationToken cancellationToken = default)
{
    return chatClient.CompleteChat(messages, options, cancellationToken);
}

public static async Task<ParsedChatCompletion<T?>> CompleteChatAsync<T>(
    this ChatClient chatClient,
    List<ChatMessage> messages,
    ChatCompletionOptions? options = null,
    CancellationToken cancellationToken = default)
{
    return await chatClient.CompleteChatAsync(messages, options, cancellationToken);
}

public static string ModelJsonSchema(this Type t)
{
    return OpenAIJsonSchema.For(t);
}
