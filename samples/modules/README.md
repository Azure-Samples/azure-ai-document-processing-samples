# Document Processing with Azure AI Samples - Python Modules

This folder contains a collection of Python classes that are used by the samples. Their purpose is to provide reusable code and patterns for structured outputs as data transfer objects (DTOs), as well as evaluators for comparing the results of data extraction techniques.

## Modules

- [App Settings](./app_settings.py) - Contains a simple class to access environment variables for the samples.
- [Data Extraction Result](./data_extraction_result.py) - Contains a class to wrap the results of the data extraction process, including the data, the accuracy, execution time, and token consumption.
- [Stopwatch](./stopwatch.py) - Contains a simple class to measure the execution time of a block of code.
- [Invoice](./invoice.py) - Contains models for representing invoice data extracted from documents and an evaluator to compare the results between the ground truth and the extracted data.
- [VehicleInsurancePolicy](./vehicle_insurance_policy.py) - Contains models for representing vehicle insurance policy data extracted from documents and an evaluator to compare the results between the ground truth and the extracted data.
