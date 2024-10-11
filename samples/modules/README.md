# Document Processing with Azure AI Samples - Python Modules

This folder contains a collection of Python classes that are used by the samples. Their purpose is to provide reusable code and patterns for structured outputs as data transfer objects (DTOs), as well as evaluators for comparing the results of data extraction techniques.

## Helper Modules

- [App Settings](./app_settings.py) - Contains a simple class to access environment variables for the samples.
- [Comparison](./comparison.py) - Contains helper functions to compare the results of data extraction and classification techniques to render the results.
- [Confidence](./confidence.py) - Contains shared helper functions for retrieving confidence scores from service specific confidence evaluation results.
  - [AI Document Intelligence Confidence](./document_intelligence_confidence.py) - Contains helper functions to evaluate the confidence of a structured output using a language model against the layout analysis result from Azure AI Document Intelligence.
  - [Marker/Surya Confidence](./marker_surya_confidence.py) - Contains helper functions to evaluate the confidence of a structured output using a language model against the OCR analysis result from the Surya OCR model.
  - [OpenAI Confidence](./openai_confidence.py) - Contains helper functions to evaluate the confidence of a structured output from the GPT-4o model against the [`logprobs`](https://learn.microsoft.com/en-us/azure/ai-services/openai/reference#request-body:~:text=False-,logprobs,-integer) result from the OpenAI API response.
- [Document Processing Results](./document_processing_result.py) - Contains classes to wrap the results of the data extraction and classification processes, including the data, the confidence, the accuracy, execution time, and token consumption.
- [Marker/Surya Extensions](./marker_surya_extensions.py) - Contains an extension over Marker's default Markdown analysis function to return the results of the Surya OCR analysis.
- [Serialization](./serialization.py) - Contains a custom JSON encoder to serialize objects that contain a `to_dict`, `as_dict`, or `model_dump` function.
- [Stopwatch](./stopwatch.py) - Contains a simple class to measure the execution time of a block of code.
- [Validation](./validation.py) - Contains helper functions to validate field values extracted from documents.

## Structured Output Modules

- [Classification](./classification.py) - Contains models representing classifications for pages of a document.
- [Invoice](./invoice.py) - Contains models representing invoice data extracted from documents and an evaluator to compare the results between the ground truth and the extracted data.
- [VehicleInsurancePolicy](./vehicle_insurance_policy.py) - Contains models representing vehicle insurance policy data extracted from documents and an evaluator to compare the results between the ground truth and the extracted data.
