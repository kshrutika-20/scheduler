from abc import ABC, abstractmethod
from typing import List

class BaseAdapter(ABC):
  @abstractmethod
  def fetch_records(self) -> List[dict]:
    pass

  @abstractmethod
  def post_process(self, records: List[dict]):
    pass
