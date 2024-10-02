import time


class Stopwatch:
    elapsed = 0
    is_running = False

    def reset(self):
        self.elapsed = 0
        self.is_running = False

    def start(self):
        if self.is_running:
            return

        self.is_running = True
        self.start_time = time.perf_counter()

    def stop(self):
        if not self.is_running:
            return

        self.is_running = False
        self.elapsed = time.perf_counter() - self.start_time
