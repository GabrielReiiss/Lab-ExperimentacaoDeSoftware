"""
Spinner de terminal: indicador visual (/ - \\ |) pra operações que ficam
bloqueadas esperando.
"""
import itertools
import sys
import threading
import time

FRAMES = ["/", "-", "\\", "|"]
INTERVAL_SECONDS = 0.1

class Spinner:
    def __init__(self, message: str):
        self._message = message
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._spin, daemon=True)

    def _spin(self) -> None:
        for frame in itertools.cycle(FRAMES):
            if self._stop_event.is_set():
                break
            sys.stdout.write(f"\r{frame} {self._message}")
            sys.stdout.flush()
            time.sleep(INTERVAL_SECONDS)

    def __enter__(self) -> "Spinner":
        self._thread.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self._stop_event.set()
        self._thread.join()
        sys.stdout.write("\r" + " " * (len(self._message) + 2) + "\r")
        sys.stdout.flush()
