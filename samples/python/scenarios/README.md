# Document Processing with Azure AI Samples - Use Case Scenarios

This folder contains a collection of end-to-end use case scenarios that demonstrate how to combine the various Python samples to create a real-world scenario for document processing.

## Scenarios

| Document Type                                            | Description                                                                                                                                                                                                                                     |
| -------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [**Invoice**](./invoices/invoice-extraction.ipynb)       | Using a [structured Invoice object](../modules/samples/models/invoice.py), invoice documents can be extracted into a standard Invoice schema by first classifying which pages to extract from using boundary detection.                         |
| [**US Tax 1040**](./us_tax/us-tax-1040-extraction.ipynb) | Using Azure AI Document Intelligence prebuilt-tax.us.1040 models, US Tax 1040 documents can be extracted into a standard schema for each form type by first classifying which pages to extract from using boundary detection with Azure OpenAI. |
