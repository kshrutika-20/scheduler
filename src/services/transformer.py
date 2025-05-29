import requests
from utils.logger import get_logger
from services.parallel_executor import ParallelExecutor

logger = get_logger(__name__)

class Transformer:
  def __init__(self, transformation_api_url: str, parallel_executor: ParallelExecutor):
    self.transformation_api_url = transformation_api_url
    self.parallel_executor = parallel_executor

  def _transform_record(self, record: dict) -> bool:
    try:
      response = requests.post(self.transformation_api_url)
      return response.status_code == 200
    except requests.RequestException as e:
      logger.error(f"Failed to transform record {record.get('_id', 'unknown')}: {e}")
      return False

  def transform_records(self, records: list[dict]) -> list[bool]:
    return self.parallel_executor.execute(self._transform_record, records)
