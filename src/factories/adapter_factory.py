from src.adapters.mongo_adapter import MongoAdapter
from src.adapters.graphql_adapter import GraphQLAdapter

class AdapterFactory:
    @staticmethod
    def create(adapter_type, executor, **kwargs):
        if adapter_type == "mongo":
            return MongoAdapter(executor, **kwargs)
        elif adapter_type == "graphql":
            return GraphQLAdapter(executor, **kwargs)
        else:
            raise ValueError(f"Unsupported adapter type: {adapter_type}")
