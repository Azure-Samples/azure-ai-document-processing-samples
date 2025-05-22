from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field


class Classification(BaseModel):
    """
    A class representing a classification of a collection of page images from a document.
    """

    classification: Optional[str] = Field(
        description='Classification of the page, e.g., invoice, receipt, etc.'
    )
    image_range_start: Optional[int] = Field(
        description='If a single document associated with the classification spans multiple pages, this field specifies the start of the image range, e.g., 1.'
    )
    image_range_end: Optional[int] = Field(
        description='If a single document associated with the classification spans multiple pages, this field specifies the end of the image range, e.g., 20.'
    )


class Classifications(BaseModel):
    """
    A class representing a list of document page image classifications.
    """

    classifications: list[Classification] = Field(
        description='List of document page image classifications.'
    )
