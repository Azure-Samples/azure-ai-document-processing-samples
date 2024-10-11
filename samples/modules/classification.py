from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field


class ClassificationBase(BaseModel):
    """
    A class representing a classification of a page.

    Attributes:
        page_number: The page number of the classification.
        classification: The classification of the page.
    """

    page_number: Optional[int] = Field(
        description='The page number of the classification.'
    )
    classification: Optional[str] = Field(
        description='The classification of the page.'
    )

    @staticmethod
    def example():
        """
        Returns an empty example ClassificationBase object with default values.

        Returns:
            ClassificationBase: An empty ClassificationBase object.
        """

        return ClassificationBase(
            page_number=1,
            classification=''
        )

    def to_dict(self):
        """
        Converts the ClassificationBase object to a dictionary.

        Returns:
            dict: The ClassificationBase object as a dictionary.
        """

        return {
            'classification': self.classification
        }


class Classification(ClassificationBase):
    """
    A class representing a classification of a page with additional metadata.

    Attributes:
        page_number: The page number of the classification.
        classification: The classification of the page.
        similarity: The similarity of the classification from 0 to 100.
        all_similarities: The similarities of all the classifications.
    """

    similarity: Optional[float] = Field(
        description='The similarity of the classification from 0 to 100.'
    )
    all_similarities: Optional[list[dict[str, str]]] = Field(
        description='The similarities of all the classifications.'
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
            similarity=0,
            all_similarities=[{'classification': '', 'similarity': 0}]
        )

    def to_dict(self):
        """
        Converts the Classification object to a dictionary.

        Returns:
            dict: The Classification object as a dictionary.
        """

        return super().to_dict()


class Classifications(BaseModel):
    """
    A class representing a list of classifications.

    Attributes:
        classifications: The list of Classification objects.
    """

    classifications: list[ClassificationBase] = Field(
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
            classifications=[ClassificationBase.example()]
        )

    def get_classification(self, page_number: int):
        """
        Gets the classification for a specific page number.

        Args:
            page_number: The page number to get the classification for.

        Returns:
            ClassificationBase: The classification for the specified page number.
        """

        classification_dict = {c.page_number: c for c in self.classifications}
        return classification_dict.get(page_number, None)

    def to_dict(self):
        """
        Converts the Classifications object to a dictionary.

        Returns:
            dict: The Classifications object as a dictionary.
        """

        return {
            'classifications': [classification.to_dict() for classification in self.classifications]
        }
