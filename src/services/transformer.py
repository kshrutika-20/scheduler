import logging
import requests

logger = logging.getLogger(__name__)

class Transformer:
    def __init__(self, api_url, executor):
        self.api_url = api_url
        self.executor = executor

    def _transform_record(self, record):
        try:
            response = requests.post(self.api_url, json=record)
            response.raise_for_status()
            result = response.json()
            success = result.get("success", False)
            if not success:
                logger.warning(f"Transformation failed for record ID {record.get('_id', record)}: {result}")
            return success
        except Exception as e:
            logger.exception(f"Exception during transformation of record ID {record.get('_id', record)}: {e}")
            return False

    def transform_records(self, records):
        return self.executor.execute(self._transform_record, records)