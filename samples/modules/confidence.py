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
