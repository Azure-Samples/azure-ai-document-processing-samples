from azure.core.credentials import TokenCredential
import requests
from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime


class AnalyzeResultError(BaseModel):
    id: str
    error: dict


class AnalyzeResultDocumentLocation(BaseModel):
    kind: str
    location: str


class AnalyzeResultDocument(BaseModel):
    id: str
    source: AnalyzeResultDocumentLocation
    targets: List[AnalyzeResultDocumentLocation]
    warnings: Optional[List[str]]


class AnalyzeResultTaskResults(BaseModel):
    documents: List[AnalyzeResultDocument]
    errors: Optional[List[AnalyzeResultError]]
    modelVersion: str


class AnalyzeResultTaskItem(BaseModel):
    kind: str
    taskName: str
    lastUpdateDateTime: datetime
    status: str
    results: AnalyzeResultTaskResults


class AnalyzeResultTasks(BaseModel):
    completed: int
    failed: int
    inProgress: int
    total: int
    items: List[AnalyzeResultTaskItem]


class AnalyzeResult(BaseModel):
    jobId: str
    lastUpdatedDateTime: datetime
    createdDateTime: datetime
    expirationDateTime: datetime
    status: str
    errors: Optional[List[AnalyzeResultError]]
    displayName: str
    tasks: AnalyzeResultTasks


class AnalyzeDocumentRequestInputDocumentLocation(BaseModel):
    location: str


class AnalyzeDocumentRequestInputDocument(BaseModel):
    language: str
    id: str
    source: AnalyzeDocumentRequestInputDocumentLocation
    target: AnalyzeDocumentRequestInputDocumentLocation


class AnalyzeDocumentRequestInput(BaseModel):
    documents: List[AnalyzeDocumentRequestInputDocument]


class AnalyzeDocumentRequestTaskRedactionPolicy(BaseModel):
    policy_kind: Literal["noMask", "characterMask", "entityMask"] = Field(
        "characterMask", alias="policyKind")


class AnalyzeDocumentRequestTaskParameters(BaseModel):
    redaction_policy: AnalyzeDocumentRequestTaskRedactionPolicy = Field(
        alias="redactionPolicy")
    pii_categories: List[str] = Field(alias="piiCategories")
    exclude_extraction_data: bool = Field(False, alias="excludeExtractionData")


class AnalyzeDocumentRequestTask(BaseModel):
    kind: Literal["PiiEntityRecognition"]
    task_name: str = Field(alias="taskName")
    parameters: AnalyzeDocumentRequestTaskParameters


class AnalyzeDocumentRequest(BaseModel):
    display_name: str = Field(alias="displayName")
    analysis_input: AnalyzeDocumentRequestInput = Field(alias="analysisInput")
    tasks: List[AnalyzeDocumentRequestTask]


class LanguageNativePIIClient:
    """
    A class for interacting with the Azure AI Language Native PII APIs.
    """

    def __init__(self, endpoint: str, credential: TokenCredential):
        """
        Initializes a new instance of the LanguageNativePIIClient class.

        Args:
            endpoint (str): The endpoint of the Azure AI Language service.
            credential (TokenCredential): The credential to use for authentication.
        """

        self._endpoint = endpoint
        self._credential = credential

    def begin_analyze_document(
        self,
        analyze_request: AnalyzeDocumentRequest
    ) -> AnalyzeResult:
        """
        Initiates an analyze document operation.

        Args:
            analyze_request (AnalyzeDocumentRequest): The request to analyze the document.
        """

        # Get a bearer token for the request
        access_token = self._credential.get_token(
            "https://cognitiveservices.azure.com/.default")

        # Initiate the analyze document request
        response = requests.post(
            f"{self._endpoint}/language/analyze-documents/jobs?api-version=2024-11-15-preview",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token.token}"
            },
            json=analyze_request
        )

        status = response.status_code
        operation_location = response.headers.get("operation-location")

        # Poll the operation location until the operation is complete
        finished = False

        while not finished:
            response = requests.get(
                operation_location,
                headers={
                    "Authorization": f"Bearer {access_token.token}"
                }
            )

            status = response.status_code
            analyze_result = AnalyzeResult.model_validate(response.json())

            if status == 200:
                if analyze_result.status == "succeeded":
                    finished = True

                    if analyze_result.errors:
                        raise Exception(analyze_result.errors)

                    if analyze_result.tasks.failed > 0:
                        raise Exception("Analyze operation failed")

                    for task in analyze_result.tasks.items:
                        if task.results.errors:
                            raise Exception(task.results.errors)

        return analyze_result
