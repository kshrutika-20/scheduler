from src.adapters.mongo_adapter import MongoAdapter
from src.adapters.graphql_adapter import GraphQLAdapter
from src.adapters.base_adapter import BaseAdapter

class AdapterFactory:
  @staticmethod
  def create_adapter(adapter_type: str, executor=None, **kwargs) -> BaseAdapter:
    if adapter_type == "mongo":
      return MongoAdapter(kwargs["uri"], kwargs["database"], kwargs["collection"])
    elif adapter_type == "graphql":
      return GraphQLAdapter(
        endpoint=kwargs["endpoint"],
        executor=executor,
        query_template=kwargs["query_template"],
        mutation_template=kwargs["mutation_template"]
      )
    else:
      raise ValueError(f"Unsupported adapter type: {adapter_type}")