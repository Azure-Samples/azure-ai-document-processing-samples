# Document Processing with Azure AI Samples - Module

This folder contains a collection of Python classes that are used by the Python samples. Their purpose is to provide reusable code and patterns for structured outputs as data transfer objects (DTOs), as well as evaluators for comparing the results of data extraction techniques.

## Helper Classes

- [Accuracy Evaluator](./samples/evaluation/accuracy_evaluator.py) - Contains a generic class for evaluating the accuracy of the comparison between any two objects.
- [App Settings](./samples/app_settings.py) - Contains a simple class to access environment variables for the samples.
- [Comparison](./samples/evaluation/comparison.py) - Contains helper functions to compare the results of data extraction and classification techniques to render the results.
- [Confidence](./samples/confidence/confidence_utils.py) - Contains shared helper functions for retrieving confidence scores from service specific confidence evaluation results.
  - [AI Document Intelligence Confidence](./samples/confidence/document_intelligence_confidence.py) - Contains helper functions to evaluate the confidence of a structured output using a language model against the layout analysis result from Azure AI Document Intelligence.
  - [OpenAI Confidence](./samples/confidence/openai_confidence.py) - Contains helper functions to evaluate the confidence of the output from a GPT model against the [`logprobs`](https://learn.microsoft.com/en-us/azure/ai-services/openai/reference#request-body:~:text=False-,logprobs,-integer) result from the OpenAI API response.
- [Document Processing Results](./samples/models/document_processing_result.py) - Contains classes to wrap the results of the data extraction and classification processes, including the data, the confidence, the accuracy, execution time, and token consumption.
- Utils - Contains the following:
  - [`CustomJsonEncoder`](./samples/utils/custom_json_encoder.py) - A custom JSON encoder to serialize objects that contain a `to_dict`, `as_dict`, or `model_dump` function.
  - [`Stopwatch`](./samples/utils/stopwatch.py) - A simple class to measure the execution time of a block of code.
  - [`Storage Utils`](./samples/utils/storage_utils.py) - Includes functions to create directories and files.
  - [`Value Utils`](./samples/utils/value_utils.py) - Includes functions to flatten a nested dictionary, to check if two values are equal, and to check if a value contains another value.

## Structured Output Classes

- [Classification](./samples/models/classification.py) - Contains models representing classifications for pages of a document.
- [Redaction](./samples/models/redaction.py) - Contains models representing redactions for pages of a document.
- [Invoice](./samples/models/invoice.py) - Contains models representing invoice data extracted from documents and an evaluator to compare the results between the ground truth and the extracted data.
- [VehicleInsurancePolicy](./samples/models/vehicle_insurance_policy.py) - Contains models representing vehicle insurance policy data extracted from documents and an evaluator to compare the results between the ground truth and the extracted data.
