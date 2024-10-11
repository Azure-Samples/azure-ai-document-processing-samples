import copy
from typing import Iterable, Optional
from marker.schema.page import Page
from marker.schema.block import Span
from modules.confidence import get_confidence_values
from modules.validation import value_contains, value_match


class MLine():
    """
    A class representing a line in a document extracted by Marker with additional metadata.
    """

    def __init__(
        self,
        bbox: list[float],
        spans: list[Span],
        normalized_polygon: Optional[list[dict[str, int]]],
        confidence: float,
        page_number: int,
        contained_words: Optional[list[str]] = None,
    ) -> None:
        """
        Initializes a new instance of the MLine class based on a Line instance.

        Args:
            normalized_polygon: The normalized polygon of the line.
            confidence: The confidence score of the line.
            page_number: The page number of the line.
        """

        self.bbox = bbox
        self.spans = spans
        self.normalized_polygon = normalized_polygon
        self.confidence = confidence
        self.page_number = page_number
        self.contained_words = contained_words

    bbox: list[float]
    spans: list[Span]
    normalized_polygon: Optional[list[dict[str, int]]]
    confidence: float
    page_number: int
    contained_words: Optional[list[str]]

    def to_dict(self) -> dict:
        """
        Converts the MLine instance to a dictionary.

        Returns:
            dict: The MLine instance as a dictionary.
        """

        return {
            'bbox': self.bbox,
            'spans': [span.model_dump() for span in self.spans],
            'normalized_polygon': self.normalized_polygon,
            'confidence': self.confidence,
            'page_number': self.page_number,
            'contained_words': self.contained_words
        }


def normalize_polygon(
    page: Page,
    polygon: list[float]
) -> list[float]:
    """
    Normalize a polygon's coordinates to page dimensions.
    The polygon is represented the top left, and bottom right corners of the bounding box as [x1, y1, x2, y2].

    Args:
        page: The page containing the polygon.
        polygon: The polygon to normalize.

    Returns:
        list: The normalized polygon coordinates as [x1, y1, x2, y2].
    """

    result = list()

    for i in range(0, len(polygon), 2):
        x = polygon[i]
        y = polygon[i + 1]

        # Normalize the coordinates to the page dimensions
        x = round(x / page.width, 3)
        y = round(y / page.height, 3)

        result.append(x)
        result.append(y)

    return result


def bbox_intersect(
    bbox_a: list[float],
    bbox_b: list[float]
) -> bool:
    """
    Checks if two bounding boxes intersect.

    Args:
        bbox_a: The first bounding box.
        bbox_b: The second bounding box.

    Returns:
        bool: True if the bounding boxes intersect, False otherwise.
    """

    x1_a, y1_a, x2_a, y2_a = bbox_a
    x1_b, y1_b, x2_b, y2_b = bbox_b

    return not (x2_a < x1_b or x1_a > x2_b or y2_a < y1_b or y1_a > y2_b)


def extract_lines(
    pages: list[Page],
    multiple_score_resolver: callable = min
) -> list[MLine]:
    m_lines = list()

    for page_number, page in enumerate(pages):
        confidence_bboxes = page.text_lines.bboxes

        for block in page.blocks:
            for line in block.lines:
                contained_words_conf_scores = list()

                line_copy = copy.copy(line)
                contained_words = list()
                for span in line_copy.spans:
                    contained_words.append(span.text)
                    # Get the confidence_bbox where the span is contained
                    for confidence_bbox in confidence_bboxes:
                        if bbox_intersect(confidence_bbox.bbox, span.bbox):
                            contained_words_conf_scores.append(
                                confidence_bbox.confidence)
                    if not contained_words_conf_scores:
                        contained_words_conf_scores.append(0)

                m_line = MLine(
                    spans=line_copy.spans,
                    bbox=line_copy.bbox,
                    contained_words=contained_words,
                    page_number=page_number,
                    confidence=multiple_score_resolver(
                        contained_words_conf_scores
                    ),
                    normalized_polygon=normalize_polygon(
                        page, line.bbox
                    )
                )
                m_lines.append(m_line)
    return m_lines


def find_matching_lines(
    value: any,
    pages: list[Page],
    value_matcher: callable = value_match,
    multiple_score_resolver: callable = min
) -> list[MLine]:
    """
    Find lines in the Marker/Surya pages that match a given value.

    Args:
        value: The value to match.
        pages: The pages to search for matching lines.
        value_matcher: The function to use for matching values.
        multiple_score_resolver: The function to use for resolving multiple confidence scores.

    Returns:
        list: The list of matching lines.
    """

    if not value:
        return list()

    if not isinstance(value, str):
        value = str(value)

    m_lines = extract_lines(pages, multiple_score_resolver)

    matching_lines = list()
    for m_line in m_lines:
        for word in m_line.contained_words:
            if value_matcher(value, word):
                matching_lines.append(m_line)

    return matching_lines


def finalize_confidence_score(
    scores: Iterable[float],
    default_score: Optional[float | int] = None,
    multiple_score_resolver: callable = min
) -> float:
    """
    Determines the final confidence score based on multiple scores.

    Args:
        scores: The list of confidence scores.
        default_score: The default score to use if no scores are provided.
        multiple_score_resolver: The function to use for resolving multiple confidence scores.

    Returns:
        float: The final confidence score.
    """

    if len(scores) == 1:
        return scores[0]
    if len(scores) == 0:
        return default_score
    return multiple_score_resolver(scores)


def evaluate_confidence(
    extract_result: dict,
    pages: list[Page],
):
    """
    Evalute the confidence of extracted fields based on the Marker/Surya pages.

    Args:
        extract_result: The extraction result.
        pages: The pages to use for evaluation.

    Returns:
        dict: The confidence evaluation of the extraction result.
    """

    def evaluate_field_value_confidence(
        value: any,
    ) -> dict:
        """
        Evaluate the confidence of a field value based on the Marker/Surya pages.

        Args:
            value: The value to evaluate.

        Returns:
            dict: The confidence evaluation of the value.
        """

        if isinstance(value, dict):
            # Recursively evaluate confidence for nested values
            return {
                key: evaluate_field_value_confidence(val)
                for key, val in value.items()
            }
        elif isinstance(value, list):
            # Evaluate confidence for each item in the list
            return [
                evaluate_field_value_confidence(item)
                for item in value
            ]
        else:
            # Find lines that match the value exactly or contain the value
            matching_lines = find_matching_lines(
                value,
                pages,
                value_matcher=value_match)
            if not matching_lines:
                matching_lines = find_matching_lines(
                    value,
                    pages,
                    value_matcher=value_contains)

            # Calculate the confidence score based on the matching lines
            field_confidence_score = finalize_confidence_score(
                scores=[match.confidence for match in matching_lines],
                default_score=0.0,
                multiple_score_resolver=max
            )

            normalized_polygons = [
                line.normalized_polygon for line in matching_lines
            ]

            return {
                "confidence": field_confidence_score,
                "matching_lines": matching_lines,
                "normalized_polygons": normalized_polygons,
                "value": value
            }

    confidence = dict()

    for field, value in extract_result.items():
        confidence[field] = evaluate_field_value_confidence(value)

    confidence_scores = get_confidence_values(confidence)

    if confidence_scores:
        confidence['_overall'] = sum(
            confidence_scores) / len(confidence_scores)
    else:
        confidence['_overall'] = 0.0

    return confidence
