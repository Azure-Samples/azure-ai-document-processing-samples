from __future__ import annotations
from typing import Optional
from pydantic import BaseModel


class Classification(BaseModel):
    page_number: Optional[int]
    classification: Optional[str]

    @staticmethod
    def empty():
        return Classification(
            page_number=1,
            classification=''
        )

    def to_dict(self):
        return {
            'page_number': self.page_number,
            'classification': self.classification
        }


class Classifications(BaseModel):
    classifications: list[Classification]

    @staticmethod
    def empty():
        return Classifications(
            classifications=[Classification.empty()]
        )

    def to_dict(self):
        return {
            'classifications': [classification.to_dict() for classification in self.classifications]
        }
