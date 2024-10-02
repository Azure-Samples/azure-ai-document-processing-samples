from __future__ import annotations
import json
from typing import Optional


class DataExtractionResult:
    def __init__(self, data: Optional[dict], accuracy: Optional[dict], prompt_tokens: Optional[int], completion_tokens: Optional[int], execution_time: Optional[float]):
        self.data = data
        self.accuracy = accuracy
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens
        self.execution_time = execution_time

    def to_json(self, indent: Optional[int] = 4) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    def to_dict(self) -> dict:
        return {
            'data': self.data,
            'accuracy': self.accuracy,
            'prompt_tokens': self.prompt_tokens,
            'completion_tokens': self.completion_tokens,
            'execution_time': self.execution_time
        }
