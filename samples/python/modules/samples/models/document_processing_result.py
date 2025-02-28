from __future__ import annotations
from typing import Optional


class DataExtractionResult:
    """
    A class representing the result of data extraction.

    Attributes:
        extract_result: The extracted data.
        confidence: The confidence of the extracted data.
        accuracy: The accuracy of the extracted data.
        prompt_tokens: The number of tokens in the prompt.
        completion_tokens: The number of tokens in the completion.
        execution_time: The execution time of the data extraction.
    """

    def __init__(
            self,
            extract_result: Optional[dict],
            confidence: Optional[dict],
            accuracy: Optional[dict],
            prompt_tokens: Optional[int],
            completion_tokens: Optional[int],
            execution_time: Optional[float]
    ):
        """
        Initializes a new instance of the DataExtractionResult class.

        Args:
            extract_result: The extracted data.
            confidence: The confidence of the extracted data.
            accuracy: The accuracy of the extracted data.
            prompt_tokens: The number of tokens in the prompt.
            completion_tokens: The number of tokens in the completion.
            execution_time: The execution time of the data extraction.
        """

        self.data = extract_result
        self.confidence = confidence
        self.accuracy = accuracy
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens
        self.execution_time = execution_time

    def to_dict(self) -> dict:
        """
        Converts the DataExtractionResult object to a dictionary.

        Returns:
            dict: The DataExtractionResult object as a dictionary.
        """

        return {
            'data': self.data,
            'confidence': self.confidence,
            'accuracy': self.accuracy,
            'prompt_tokens': self.prompt_tokens,
            'completion_tokens': self.completion_tokens,
            'execution_time': self.execution_time
        }


class DataClassificationResult:
    """
    A class representing the result of data classification.

    Attributes:
        classification: The classification of the data.
        accuracy: The accuracy of the classification.
        execution_time: The execution time of the data classification.
    """

    def __init__(
            self,
            classification: Optional[dict],
            accuracy: Optional[float],
            execution_time: Optional[float]
    ):
        """
        Initializes a new instance of the DataClassificationResult class.

        Args:
            classification: The classification of the data.
            accuracy: The accuracy of the classification.
            execution_time: The execution time of the data classification.
        """

        self.classification = classification
        self.accuracy = accuracy
        self.execution_time = execution_time

    def to_dict(self) -> dict:
        """
        Converts the DataClassificationResult object to a dictionary.

        Returns:
            dict: The DataClassificationResult object as a dictionary.
        """

        return {
            'classification': self.classification,
            'accuracy': self.accuracy,
            'execution_time': self.execution_time
        }


class DataRedactionResult:
    """
    A class representing the result of data redaction.

    Attributes:
        redacted: The redaction of the data.
        execution_time: The execution time of the data redaction.
    """

    def __init__(
            self,
            redacted: Optional[str],
            confidence: Optional[dict],
            execution_time: Optional[float]
    ):
        """
        Initializes a new instance of the DataRedactionResult class.

        Args:
            redacted: The redaction of the data.
            confidence: The confidence of the redacted data.
            execution_time: The execution time of the data redaction.
        """

        self.redacted = redacted
        self.confidence = confidence
        self.execution_time = execution_time

    def to_dict(self) -> dict:
        """
        Converts the DataRedactionResult object to a dictionary.

        Returns:
            dict: The DataRedactionResult object as a dictionary.
        """

        return {
            'redacted': self.redacted,
            'confidence': self.confidence,
            'execution_time': self.execution_time
        }
