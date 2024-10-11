def get_confidence_values(data, key='confidence'):
    """
    Finds all of the confidence values in a nested dictionary or list.

    Args:
        data: The nested dictionary or list to search for confidence values.
        key: The key to search for in the dictionary.

    Returns:
        list: The list of confidence values found in the nested dictionary or list.
    """

    confidence_values = []

    def recursive_search(d):
        if isinstance(d, dict):
            for k, v in d.items():
                if k == key and (v is not None and v != 0):
                    confidence_values.append(v)
                if isinstance(v, (dict, list)):
                    recursive_search(v)
        elif isinstance(d, list):
            for item in d:
                recursive_search(item)

    recursive_search(data)
    return confidence_values


def merge_confidence_values(confidence_a: dict, confidence_b: dict):
    """
    Merges to evaluations of confidence for the same set of fields as one.
    This is achieved by summing the confidence values and averaging the scores.

    Args:
        confidence_a: The first confidence evaluation.
        confidence_b: The second confidence evaluation.

    Returns:
        dict: The merged confidence evaluation.
    """

    def merge_field_confidence_value(
        field_a: any,
        field_b: any,
        score_resolver: callable = max
    ) -> dict:
        """
        Merges two field confidence values.
        If the field is a dictionary or list, the function is called recursively.

        Args:
            field_a: The first field confidence value.
            field_b: The second field confidence value.

        Returns:
            dict: The merged field confidence value.
        """

        if isinstance(field_a, dict) and 'confidence' not in field_a:
            return {
                key: merge_field_confidence_value(field_a[key], field_b[key])
                for key in field_a if not key.startswith('_')
            }
        elif isinstance(field_a, list):
            return [
                merge_field_confidence_value(field_a[i], field_b[i])
                for i in range(len(field_a))
            ]
        else:
            return {
                'confidence': score_resolver([field_a['confidence'], field_b['confidence']]),
                'value': field_a['value'] if 'field' in field_a else None
            }

    merged_confidence = merge_field_confidence_value(
        confidence_a, confidence_b)

    confidence_scores = get_confidence_values(merged_confidence)
    if confidence_scores:
        merged_confidence['_overall'] = sum(
            confidence_scores) / len(confidence_scores)
    else:
        merged_confidence['_overall'] = 0.0

    return merged_confidence
