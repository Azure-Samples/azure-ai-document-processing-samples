from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field


class RedactionWord(BaseModel):
    """
    A class representing a specific word from an OCR analysis that needs to be redacted.
    """

    polygon: list[float] = Field(
        description="The bounding box of the word to redact. Example [0.5768, 0.5639, 1.8538, 0.564, 1.8538, 0.8636, 0.5759, 0.86].")
    content: str = Field(
        description="The text content to redact.")
    category: str = Field(
        description="The category of the entity to redact, e.g. 'Name', 'Address', 'Phone Number'.")


class Redaction(BaseModel):
    """
    A class representing required data redaction from a document.
    """

    page_number: int = Field(
        description="The page number of the document.")
    words: Optional[list[RedactionWord]] = Field(
        description="Optional - The words to redact from the document.")
