import time


class Stopwatch:
    """
    A class representing a stopwatch for measuring elapsed time.

    Attributes:
        elapsed (float): The elapsed time in seconds.
        is_running (bool): A flag indicating whether the stopwatch is running
    """

    elapsed = 0
    is_running = False

    def __enter__(self):
        """
        Enters a context block and starts the stopwatch.

        Returns:
            Stopwatch: The stopwatch instance.
        """

        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exits the context block and stops the stopwatch.
        """

        self.stop()

    def reset(self):
        """
        Resets the stopwatch by setting the elapsed time to zero and stopping it
        """

        self.elapsed = 0
        self.is_running = False

    def start(self):
        """
        Starts the stopwatch by setting the start time and setting the 'is_running' flag to True.
        """

        if self.is_running:
            return

        self.is_running = True
        self.start_time = time.perf_counter()

    def stop(self):
        """
        Stops the stopwatch by calculating the elapsed time and setting the 'is_running' flag to False.
        """

        if not self.is_running:
            return

        self.is_running = False
        self.elapsed = time.perf_counter() - self.start_time
