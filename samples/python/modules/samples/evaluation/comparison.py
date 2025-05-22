import pandas as pd

from samples.utils.value_utils import flatten_dict


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
        key_confidence = confidence_flat.get(f"{key}_confidence", None)

        rows.append({
            "Field": key,
            "Expected": expected_flat.get(key),
            "Extracted": extracted_flat.get(key),
            "Confidence": f"{key_confidence * 100:.2f}%" if key_confidence else 'N/A',
            "Accuracy": f"{'Match' if accuracy_flat.get(f"{key}", 0.0) == 1.0 else 'Mismatch'}"
        })
    df = pd.DataFrame(rows)

    def highlight_row(row):
        return ['background-color: #66ff33' if row.Accuracy == 'Match' else 'background-color: #ff9999'] * len(row)

    df = df.style.apply(highlight_row, axis=1)
    return df
