from pymongo import MongoClient
from bson import ObjectId
from typing import List
from src.adapters.base_adapter import BaseAdapter

class MongoAdapter(BaseAdapter):
  def __init__(self, uri: str, database: str, collection: str):
    self.client = MongoClient(uri)
    self.db = self.client[database]
    self.collection = self.db[collection]

  def fetch_records(self) -> List[dict]:
    records = list(self.collection.find({"state": "AVAILABLE"}).limit(100))
    for record in records:
      record["_id"] = str(record["_id"])
    return records

  def post_process(self, records: List[dict]):
    ids = [ObjectId(record["_id"]) for record in records]
    self.collection.update_many({"_id": {"$in": ids}}, {"$set": {"state": "TRANSFORMED"}})
