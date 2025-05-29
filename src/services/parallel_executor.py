from concurrent.futures import ThreadPoolExecutor
from typing import Callable, List

class ParallelExecutor:
  def __init__(self, max_workers: int = 4):
    self.executor = ThreadPoolExecutor(max_workers=max_workers)

  def execute(self, func: Callable, data: List):
    futures = [self.executor.submit(func, item) for item in data]
    return [future.result() for future in futures]
