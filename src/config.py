import os

TRANSFORMATION_API_URL = os.environ.get("TRANSFORMATION_API_URL", "http://abc.com/silver-layer")
GRAPHQL_ENDPOINT = os.environ.get("GRAPHQL_ENDPOINT", "http://abc.com/graphql")
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.environ.get("DB_NAME", "mydb")
EXECUTION_MODE = os.environ.get("EXECUTION_MODE", "thread")  # or "thread"

ADAPTER_CONFIGS = [
    {
        "type": "mongo",
        "kwargs": {
            "uri": MONGO_URI,
            "database": DB_NAME,
            "collection": os.environ.get("MONGO_COLLECTION", "my_collection")
        },
        "trigger": "interval",
        "trigger_args": {"seconds": int(os.environ.get("MONGO_TRIGGER_INTERVAL", 60))}
    },
    {
        "type": "graphql",
        "kwargs": {
            "endpoint": GRAPHQL_ENDPOINT,
            "query_template": os.environ.get("GRAPHQL_QUERY_TEMPLATE", """
                query FetchIds {
                    itemsToUpdate {
                        id
                    }
                }
            """),
            "mutation_template": os.environ.get("GRAPHQL_MUTATION_TEMPLATE", """
                mutation UpdateStatus {{
                    updateStatus(id: \"{id}\", status: \"COMPLETED\") {{
                        success
                    }}
                }}
            """)
        },
        "trigger": "cron",
        "trigger_args": {"minute": os.environ.get("GRAPHQL_TRIGGER_CRON", "*/5")}
    }
]
