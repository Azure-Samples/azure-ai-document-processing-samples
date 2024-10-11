import json


class CustomEncoder(json.JSONEncoder):
    """
    A class representing a custom JSON encoder for serializing objects with custom dictionary representations.
    """

    def default(self, obj):
        """
        Serializes the object to a JSON-compatible format.
        Checks if the object has a 'to_dict', 'as_dict', or 'model_dump' method and calls it to get the dictionary representation.

        Args:
            obj: The object to serialize.

        Returns:
            str: The serialized object as a JSON-compatible format.
        """

        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        if hasattr(obj, 'as_dict'):
            return obj.as_dict()
        if hasattr(obj, 'model_dump'):
            return obj.model_dump()
        return super().default(obj)
