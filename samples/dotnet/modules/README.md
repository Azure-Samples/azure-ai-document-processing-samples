# Document Processing with Azure AI Samples - .NET Helpers

This folder contains a collection of .NET classes that are used by the .NET samples. Their purpose is to provide reusable code and patterns for structured outputs as data transfer objects (DTOs), as well as evaluators for comparing the results of data extraction techniques.

## Helper Classes

- [Accuracy Evaluator](./samples/evaluation/AccuracyEvaluator.csx) - Contains a generic class for evaluating the accuracy of the comparison between any two objects, converted to JsonDocument.
- [App Settings](./samples/AppSettings.csx) - Contains a simple class to access environment variables for the samples.
- [OpenAI Confidence](./samples/confidence/OpenAIConfidence.csx) - Contains helper methods to evaluate the confidence of the output from a GPT model against the [`logprobs`](https://learn.microsoft.com/en-us/azure/ai-services/openai/reference#request-body:~:text=False-,logprobs,-integer) result from the OpenAI API response.
- [Document Processing Results](./samples/models/DocumentProcessingResult.csx) - Contains classes to wrap the results of the data extraction and classification processes, including the data, the confidence, the accuracy, execution time, and token consumption.
- Helpers - Contains the following:
  - [OpenAI Structured Outputs Helpers](./samples/helpers/OpenAIStructuredOutputsHelpers.csx) - Contains supporting extension methods for the .NET OpenAI SDK to support Type generics for generating valid JSON schemas for the [Structured Outputs feature](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/structured-outputs?pivots=programming-language-csharp&tabs=python-secure%2Cdotnet-entra-id) (similar to the support in Python with Pydantic).
  - [`StopwatchContext`](./samples/helpers/StopwatchContext.csx) - A disposable wrapper around a `Stopwatch` to measure the execution time of a block of code.

## Structured Output Classes

- [Classification](./samples/models/Classification.csx) - Contains models representing classifications for pages of a document.
