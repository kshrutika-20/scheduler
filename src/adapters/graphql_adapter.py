import requests
from src.adapters.base_adapter import BaseAdapter
import logging

logger = logging.getLogger(__name__)

class GraphQLAdapter(BaseAdapter):
    def __init__(self, executor, endpoint, query_template, mutation_template):
        super().__init__(executor)
        self.endpoint = endpoint
        self.query_template = query_template
        self.mutation_template = mutation_template

    def fetch_records(self, *_):
        response = requests.post(self.endpoint, json={"query": self.query_template})
        response.raise_for_status()
        data = response.json()
        ids = data["data"]["itemsToUpdate"]
        return ids

    def post_process(self, records, mutation_template=None):
        mutation_template = mutation_template or self.mutation_template

        def run_mutation(item):
            id_ = item["id"]
            mutation = mutation_template.format(id=id_)
            res = requests.post(self.endpoint, json={"query": mutation})
            res.raise_for_status()
            return res.json().get("data", {}).get("updateStatus", {}).get("success", False)

        results = self.executor.execute(run_mutation, records)
        logger.info(f"GraphQL mutations complete: {sum(results)} success, {len(results)-sum(results)} failed")
