import os
import dlt

from dotenv import load_dotenv
from dlt.sources.rest_api import rest_api_resources

load_dotenv()


@dlt.source
def logfire_source():

    config = {
        "client": {
            "base_url": "https://logfire-us.pydantic.dev/v2/",
            "auth": {
                "type": "bearer",
                "token": os.getenv("LOGFIRE_READ_TOKEN"),
            },
            "headers": {
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        },
        "resources": [
            {
                "name": "query",
                "endpoint": {
                    "path": "query",
                    "method": "POST",
                    "json": {
                        "sql": """
                            SELECT *
                            FROM records
                            LIMIT 100
                        """,
                        "min_timestamp": "2026-07-01T00:00:00Z",
                    },
                },
            }
        ],
    }

    yield from rest_api_resources(config)


pipeline = dlt.pipeline(
    pipeline_name="logfire_pipeline",
    destination="duckdb",
    dataset_name="agent_traces",
)

load_info = pipeline.run(logfire_source())

print(load_info)