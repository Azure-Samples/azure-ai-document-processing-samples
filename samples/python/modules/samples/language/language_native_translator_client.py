from azure.core.credentials import TokenCredential
import requests
from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime


class AnalyzeResultError(BaseModel):
    code: str
    message: str


class AnalyzeResult(BaseModel):
    id: str
    createdDateTimeUtc: datetime
    lastActionDateTimeUtc: datetime
    status: str
    error: Optional[AnalyzeResultError]

    @staticmethod
    def from_dict(obj: dict) -> 'AnalyzeResult':
        id = obj.get("id")
        createdDateTimeUtc = obj.get("createdDateTimeUtc")
        lastActionDateTimeUtc = obj.get("lastActionDateTimeUtc")
        status = obj.get("status")
        error = obj.get("error", None)
        return AnalyzeResult(id=id, createdDateTimeUtc=createdDateTimeUtc, lastActionDateTimeUtc=lastActionDateTimeUtc, status=status, error=error)


class AnalyzeDocumentRequestInputTarget(BaseModel):
    target_url: str = Field(alias="targetUrl")
    language: str


class AnalyzeDocumentRequestInputSource(BaseModel):
    source_url: str = Field(alias="sourceUrl")
    language: Optional[str]


class AnalyzeDocumentRequestInput(BaseModel):
    storage_type: Literal["File"] = Field(alias="storageType")
    source: AnalyzeDocumentRequestInputSource
    targets: List[AnalyzeDocumentRequestInputTarget]


class AnalyzeDocumentRequest(BaseModel):
    inputs: List[AnalyzeDocumentRequestInput]


class LanguageNativeTranslatorClient:
    """
    A class for interacting with the Azure AI Language Native Translator APIs.
    """

    def __init__(self, endpoint: str, credential: TokenCredential):
        """
        Initializes a new instance of the LanguageNativeTranslatorClient class.

        Args:
            endpoint (str): The endpoint of the Azure AI Translator service.
            credential (TokenCredential): The credential to use for authentication.
        """

        self._endpoint = endpoint
        self._credential = credential

    def begin_analyze_document(
        self,
        analyze_request: AnalyzeDocumentRequest
    ):
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
            f"{self._endpoint}/translator/text/batch/v1.1/batches",
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
            response_json = response.json()

            analyze_result = AnalyzeResult.from_dict(response_json)

            if status == 200:
                if analyze_result.status.lower() == "succeeded" or analyze_result.error:
                    finished = True

                    if analyze_result.error:
                        raise Exception(
                            f"Analyze operation failed: {analyze_result.error.code} - {analyze_result.error.message}")

        return analyze_result
