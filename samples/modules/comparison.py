from typing import Optional
import pandas as pd

from modules.classification import Classifications


def flatten_dict(data, parent_key='', sep='_'):
    """
    Flatten a nested dictionary.

    Args:
        data: The dictionary to flatten.
        parent_key: The parent key.
        sep: The separator to use between keys.

    Returns:
        dict: The flattened dictionary with keys separated by the separator.
    """

    items = []
    for k, v in data.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            for i, item in enumerate(v):
                items.extend(flatten_dict(
                    {f"{new_key}_{i}": item}, '', sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def highlight_comparison(actual_value, expected_value):
    """
    Highlight the comparison of two values by coloring them green if they match and red if they don't.

    Args:
        actual_value: The actual value.
        expected_value: The expected value.

    Returns:
        str: The highlighted comparison of the two values.
    """

    if isinstance(actual_value, dict) and isinstance(expected_value, dict):
        return {k: highlight_comparison(actual_value.get(k), expected_value.get(k)) for k in expected_value.keys()}
    elif isinstance(actual_value, list) and isinstance(expected_value, list):
        return [highlight_comparison(v, ev) for v, ev in zip(actual_value, expected_value)]
    else:
        if isinstance(actual_value, str) and isinstance(expected_value, str) and actual_value.lower() == expected_value.lower():
            return f"<span style='color: green'>{actual_value}</span>"
        elif actual_value == expected_value:
            return f"<span style='color: green'>{actual_value}</span>"
        else:
            return f"<span style='color: red'>{actual_value}</span>"


def extraction_comparison(expected: dict, extracted: dict, confidence: dict):
    """
    Generate a markdown table comparing the extracted data with the expected data.
    Matching values are highlighted in green, while non-matching values are highlighted in red.

    Args:
        expected: The expected data.
        extracted: The extracted data.
        confidence: The confidence data for the extracted data.

    Returns:
        str: The markdown table comparing the extracted data with the expected data.
    """

    expected_flat = flatten_dict(expected)
    extracted_flat = flatten_dict(extracted)
    confidence_flat = flatten_dict(confidence)

    rows = []
    for key in expected_flat.keys():
        rows.append({
            "Field": key,
            "Expected": expected_flat[key],
            "Extracted": highlight_comparison(extracted_flat.get(key), expected_flat[key]),
            "Confidence": confidence_flat.get(f"{key}_confidence", None)
        })
    df = pd.DataFrame(rows)
    return df.to_markdown(index=False, tablefmt="unsafehtml")


def classification_comparison(expected: Classifications, extracted: Classifications, confidence: Optional[dict] = None):
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
            "Extracted": highlight_comparison(extracted_classification.classification, classification.classification)
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
