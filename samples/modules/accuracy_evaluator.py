class AccuracyEvaluator:
    """
    A class for evaluating the accuracy of the comparison between two objects.

    Attributes:
        match_keys (list[str]): The list of keys to use for matching objects in a list.
        total_matches (int): The total number of matches found.
        total_comparisons (int): The total number of comparisons made.
        ignore_keys (list[str]): The list of keys to ignore during comparison.
    """

    def __init__(self, match_keys: list[str] = None, ignore_keys: list[str] = None):
        """
        Initializes a new instance of the AccuracyEvaluator class.

        Args:
            match_keys (list[str]): The list of keys to use for matching objects in a list.
            ignore_keys (list[str]): The list of keys to ignore during comparison.
        """

        self.match_keys = match_keys or []
        self.ignore_keys = ignore_keys or []
        self.total_matches = 0
        self.total_comparisons = 0

    def evaluate(self, expected, actual):
        """
        Evaluates the accuracy of the comparison between two objects.

        Args:
            expected: The expected object.
            actual: The actual object.
        """

        accuracy = self._compare_objects(expected, actual)
        if self.total_comparisons == 0:
            overall_accuracy = 1.0  # If nothing to compare, treat as accurate
        else:
            overall_accuracy = self.total_matches / self.total_comparisons
        return {'accuracy': accuracy, 'overall': overall_accuracy}

    def _compare_objects(self, expected, actual):
        if isinstance(expected, dict):
            accuracy = {}
            for key, exp_val in expected.items():
                if key in self.ignore_keys:
                    continue  # Skip keys that are in the ignore_keys list
                act_val = actual.get(key) if isinstance(actual, dict) else None
                accuracy[key] = self._compare_objects(exp_val, act_val)
            return accuracy

        elif isinstance(expected, list):
            if not isinstance(actual, list):
                # All expected items are mismatches
                self.total_comparisons += len(expected)
                return [0 for _ in expected]

            accuracy_list = []
            used_indices = set()  # To keep track of matched actual items

            for exp_item in expected:
                match_found = False
                matched_accuracy = 0

                # Attempt to match using the provided match_keys
                if self.match_keys and isinstance(exp_item, dict):
                    for key in self.match_keys:
                        exp_key_val = exp_item.get(key)
                        if exp_key_val is None:
                            continue  # Skip if the expected item doesn't have this key

                        # Search for a matching actual item based on the current key
                        for idx, act_item in enumerate(actual):
                            if idx in used_indices:
                                continue  # Skip already matched items
                            act_key_val = act_item.get(key) if isinstance(
                                act_item, dict) else None
                            if act_key_val is None:
                                continue  # Skip if actual item doesn't have this key

                            # For strings, perform case-insensitive comparison
                            if isinstance(exp_key_val, str) and isinstance(act_key_val, str):
                                key_match = exp_key_val.lower() == act_key_val.lower()
                            else:
                                key_match = exp_key_val == act_key_val
                            if key_match:
                                # Match found based on the current key
                                matched_accuracy = self._compare_objects(
                                    exp_item, act_item)
                                used_indices.add(idx)
                                match_found = True
                                break
                        if match_found:
                            break  # Stop trying other keys once a match is found

                if not match_found:
                    # Attempt to match without specific keys
                    for idx, act_item in enumerate(actual):
                        if idx in used_indices:
                            continue
                        matched_accuracy = self._compare_objects(
                            exp_item, act_item)
                        if isinstance(matched_accuracy, int) and matched_accuracy == 1:
                            used_indices.add(idx)
                            match_found = True
                            break
                        elif isinstance(matched_accuracy, dict) or isinstance(matched_accuracy, list):
                            # Define a match as fully matched (all sub-attributes matched)
                            if self._is_fully_matched(matched_accuracy):
                                used_indices.add(idx)
                                match_found = True
                                break

                if match_found:
                    if isinstance(matched_accuracy, int):
                        accuracy_list.append(matched_accuracy)
                        if matched_accuracy == 1:
                            self.total_matches += 1
                        self.total_comparisons += 1
                    else:
                        # matched_accuracy is dict or list
                        accuracy_list.append(matched_accuracy)
                        # Traverse matched_accuracy to count matches and comparisons
                        matches, comparisons = self._count_matches(
                            matched_accuracy)
                        self.total_matches += matches
                        self.total_comparisons += comparisons
                else:
                    # No matching actual item found
                    accuracy_list.append(0)
                    self.total_comparisons += 1

            return accuracy_list

        else:
            # Handle primitive values
            self.total_comparisons += 1
            if expected is None and actual is None:
                self.total_matches += 1
                return 1
            if expected is None or actual is None:
                return 0

            # Handle strings (case-insensitive)
            if isinstance(expected, str) and isinstance(actual, str):
                if expected.lower() == actual.lower():
                    self.total_matches += 1
                    return 1
                else:
                    return 0

            # Handle other primitive types
            if expected == actual:
                self.total_matches += 1
                return 1
            else:
                return 0

    def _is_fully_matched(self, accuracy):
        if isinstance(accuracy, int):
            return accuracy == 1
        elif isinstance(accuracy, dict):
            return all(self._is_fully_matched(v) for v in accuracy.values())
        elif isinstance(accuracy, list):
            return all(self._is_fully_matched(v) for v in accuracy)
        else:
            return False

    def _count_matches(self, accuracy):
        if isinstance(accuracy, int):
            return (1 if accuracy == 1 else 0, 1)
        elif isinstance(accuracy, dict):
            matches = 0
            comparisons = 0
            for v in accuracy.values():
                m, c = self._count_matches(v)
                matches += m
                comparisons += c
            return (matches, comparisons)
        elif isinstance(accuracy, list):
            matches = 0
            comparisons = 0
            for v in accuracy:
                m, c = self._count_matches(v)
                matches += m
                comparisons += c
            return (matches, comparisons)
        else:
            return (0, 0)
