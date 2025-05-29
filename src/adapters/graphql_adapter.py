import requests
from typing import List
from adapters.base_adapter import BaseAdapter
from utils.logger import get_logger

logger = get_logger(__name__)

class GraphQLAdapter(BaseAdapter):
  def __init__(self, endpoint: str, executor, query_template: str, mutation_template: str):
    self.endpoint = endpoint
    self.executor = executor
    self.query_template = query_template
    self.mutation_template = mutation_template

  def fetch_records(self) -> List[dict]:
    try:
      response = requests.post(
        self.endpoint,
        json={"query": self.query_template},
        headers={"Content-Type": "application/json"}
      )
      response.raise_for_status()
      data = response.json()
      return [{"_id": item["id"]} for item in data.get("data", {}).get("itemsToUpdate", [])]
    except requests.RequestException as e:
      logger.error(f"Failed to fetch from GraphQL: {e}")
      return []

  def post_process(self, records: List[dict]):
    def run_mutation(record):
      mutation = self.mutation_template.format(id=record["_id"])
      try:
        response = requests.post(
          self.endpoint,
          json={"query": mutation},
          headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
      except requests.RequestException as e:
        logger.error(f"Failed mutation for {record['_id']}: {e}")

    self.executor.execute(run_mutation, records)
