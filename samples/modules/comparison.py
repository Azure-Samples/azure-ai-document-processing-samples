from typing import Optional
import pandas as pd

from modules.classification import Classifications
from modules.utils import flatten_dict


def get_extraction_comparison(expected: dict, actual: dict, confidence: dict, accuracy: dict):
    """
    Generate a pandas DataFrame comparing the extracted fields with the expected fields.
    If a match is found, the row is highlighted in green. If a mismatch is found, the row is highlighted in red.

    Args:
        expected: The expected fields.
        actual: The extracted fields.
        confidence: The confidence values for the extracted fields.
        accuracy: The accuracy values for the extracted fields.

    Returns:
        pd.DataFrame: The DataFrame comparing the extracted fields with the expected fields.
    """

    expected_flat = flatten_dict(expected)
    extracted_flat = flatten_dict(actual)
    confidence_flat = flatten_dict(confidence)
    accuracy_flat = flatten_dict(accuracy)

    all_keys = sorted(set(expected_flat.keys()) | set(extracted_flat.keys()))

    rows = []
    for key in all_keys:
        rows.append({
            "Field": key,
            "Expected": expected_flat.get(key),
            "Extracted": extracted_flat.get(key),
            "Confidence": f"{confidence_flat.get(f"{key}_confidence", 0.0) * 100:.2f}%",
            "Accuracy": f"{'Match' if accuracy_flat.get(f"{key}", 0.0) == 1.0 else 'Mismatch'}"
        })
    df = pd.DataFrame(rows)

    def highlight_row(row):
        return ['background-color: #66ff33' if row.Accuracy == 'Match' else 'background-color: #ff9999'] * len(row)

    df = df.style.apply(highlight_row, axis=1)
    return df


def get_classification_comparison(expected: Classifications, extracted: Classifications, confidence: Optional[dict] = None):
    """
    Generate a markdown table comparing the extracted classifications with the expected classifications.
    Matching values are highlighted in green, while non-matching values are highlighted in red.

    Args:
        expected: The expected classifications.
        extracted: The extracted classifications.
        similarities: The additional similarity data for the extracted classifications.

    Returns:
        str: The markdown table comparing the extracted classifications with the expected classifications.
    """

    def similarity_md_list(similarities: list[dict[str, str]]):
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        return "<ul>" + "".join([f"<li>{s['classification']} ({s['similarity']})</li>" for s in similarities]) + "</ul>"

    if confidence is not None:
        confidence_flat = flatten_dict(confidence)

    rows = []
    for classification in expected.classifications:
        extracted_classification = extracted.get_classification(
            classification.page_number)
        row = {
            "Page": classification.page_number,
            "Expected": classification.classification,
            "Extracted": extracted_classification.classification
        }

        # If extracted_classification is a Classification object, add extra metadata
        if hasattr(extracted_classification, 'similarity'):
            row["Similarity"] = extracted_classification.similarity
            row["Matches"] = similarity_md_list(
                extracted_classification.all_similarities)

        if confidence is not None:
            row["Confidence"] = confidence_flat.get(
                f"classifications_{classification.page_number}_classification_confidence", None)

        rows.append(row)
    df = pd.DataFrame(rows)
    return df.to_markdown(index=False, tablefmt="unsafehtml")
