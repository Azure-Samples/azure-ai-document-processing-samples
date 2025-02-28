from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field


class Classification(BaseModel):
    """
    A class representing a classification of a page.

    Attributes:
        page_number: The page number of the classification.
        classification: The classification of the page.
        similarity: The similarity of the classification from 0 to 100.
    """

    page_number: Optional[int] = Field(
        description='The page number of the classification.'
    )
    classification: Optional[str] = Field(
        description='The classification of the page.'
    )
    similarity: Optional[float] = Field(
        description='The similarity of the classification from 0 to 100.'
    )

    @staticmethod
    def example():
        """
        Returns an empty example Classification object with default values.

        Returns:
            Classification: An empty Classification object.
        """

        return Classification(
            page_number=1,
            classification='',
            similarity=0
        )


class Classifications(BaseModel):
    """
    A class representing a list of classifications.

    Attributes:
        classifications: The list of Classification objects.
    """

    classifications: list[Classification] = Field(
        description='The list of Classification objects.'
    )

    @staticmethod
    def example():
        """
        Returns an empty example Classifications object with default values.

        Returns:
            Classifications: An empty Classifications object containing an empty Classification object.
        """

        return Classifications(
            classifications=[Classification.example()]
        )

    def get_classification(self, page_number: int):
        """
        Gets the classification for a specific page number.

        Args:
            page_number: The page number to get the classification for.

        Returns:
            Classification: The classification for the specified page number.
        """

        classification_dict = {c.page_number: c for c in self.classifications}
        return classification_dict.get(page_number, None)
