from __future__ import annotations
from typing import Any, Dict, List
from azure.ai.documentintelligence.models import DocumentField

VALUE_KEY_BY_TYPE: dict[str, str | None] = {
    "string": "valueString",
    "number": "valueNumber",
    "boolean": "valueBoolean",
    "selectionGroup": "valueSelectionGroup",
    "address": "valueAddress",
    "object": None,
    "array": None,
}


def __extract(node: Any) -> Any:
    if isinstance(node, DocumentField):
        node = node.as_dict()

    if not isinstance(node, dict):
        return node

    node_type: str | None = node.get("type")

    if node_type == "object":
        inner: Dict[str, Any] = node.get("valueObject", {})
        return {k: __extract(v) for k, v in inner.items()}

    if node_type == "array":
        inner_list: List[Any] = node.get("valueArray", [])
        return [__extract(item) for item in inner_list]

    value_key = VALUE_KEY_BY_TYPE.get(node_type)
    if value_key is not None:
        if value_key in node:
            return node[value_key]
        else:
            if node_type == "string":
                return ""
            elif node_type == "number":
                return 0.0
            elif node_type == "boolean":
                return False
            elif node_type == "selectionGroup" or node_type == "array":
                return []
            elif node_type == "object" or node_type == "address":
                return {}

    for fallback in (
        "valueString",
        "valueNumber",
        "valueBoolean",
        "valueSelectionGroup",
        "valueAddress",
        "valueObject",
        "valueArray",
    ):
        if fallback in node:
            return node[fallback]

    return node


def parse_document_fields(raw_result: Dict[str, Any]) -> Dict[str, Any]:
    return {k: __extract(v) for k, v in raw_result.items()}
