SCHEDULER_INTERVAL_SECONDS = 60  # Run every 60 seconds
TRANSFORMATION_API_URL = "http://abc.com/silver-layer"
GRAPHQL_ENDPOINT = "http://abc.com/graphql"
MONGO_URI = ""
DB_NAME = ""

ADAPTER_CONFIGS = [
  {
    "type": "mongo",
    "kwargs": {
      "uri": MONGO_URI,
      "database": DB_NAME,
      "collection": "test_data"
    },
    "trigger": "interval",
    "trigger_args": {"seconds": 60}
  },
  {
    "type": "graphql",
    "kwargs": {
      "endpoint": GRAPHQL_ENDPOINT,
      "query_template": """
      query FetchIds {
        itemsToUpdate {
          id
        }
      }
      """,
      "mutation_template": """
      mutation UpdateStatus {{
        updateStatus(id: \"{id}\", status: \"COMPLETED\") {{
          success
        }}
      }}
      """
    },
    "trigger": "cron",
    "trigger_args": {"minute": "*/5"}
  }
]