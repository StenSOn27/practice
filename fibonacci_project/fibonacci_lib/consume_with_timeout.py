# from __future__ import annotations
from typing import Iterable
import time


class ConsumeWithTimeout:
    def __init__(
        self,  # noqa: ANN101
        iterable: Iterable,
        timeout_seconds: float,
        delay: float = 0.5
    ) -> None:
        self.iterable = iterable
        self.timeout_seconds = timeout_seconds
        self.delay = delay
        self.total = 0
        self.count = 0

    def __iter__(self) -> 'ConsumeWithTimeout':  # noqa: ANN101
        self.iterator = iter(self.iterable)
        self.start_time = time.time()
        self.current_element = 0
        return self

    def __next__(self) -> int:  # noqa: ANN101
        if time.time() - self.start_time >= self.timeout_seconds:
            raise StopIteration
        try:
            value = next(self.iterator)
            self.total += value
            self.count += 1
            avg = self.total / self.count
            print(
                f"Received: {value} | Sum: {self.total} | Average: {avg: .2f}"
            )
            time.sleep(self.delay)
            return value
        except StopIteration:
            raise