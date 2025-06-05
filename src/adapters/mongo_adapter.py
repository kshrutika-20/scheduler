# src/adapters/mongo_adapter.py

from pymongo import MongoClient, ReturnDocument
from src.adapters.base_adapter import BaseAdapter
import logging

logger = logging.getLogger(__name__)

class MongoAdapter(BaseAdapter):
    def __init__(self, executor, uri, database, collection):
        super().__init__(executor)
        self.client = MongoClient(uri)
        self.collection = self.client[database][collection]

    def fetch_records(self, query=None):
        final_query = query or {"status": {"$ne": "TRANSFORMED"}}
        return list(self.collection.find(final_query))

    def post_process(self, records, *args, **kwargs):
        ids = [r["_id"] for r in records]
        result = self.collection.update_many(
            {"_id": {"$in": ids}},
            {"$set": {"status": "TRANSFORMED"}}
        )
        logger.info(f"Updated {result.modified_count} MongoDB records")

    def mark_failed(self, records):
        ids = [r["_id"] for r in records]
        result = self.collection.update_many(
            {"_id": {"$in": ids}},
            {"$set": {"status": "FAILED"}}
        )
        logger.info(f"Marked {result.modified_count} records as FAILED")
