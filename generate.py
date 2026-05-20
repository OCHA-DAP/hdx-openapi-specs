"""
Assembles an OpenAPI 3.1 specification from Pydantic models and writes dist/openapi.json.
"""

import json
import sys
from pathlib import Path

from pydantic import TypeAdapter

from models.common import ErrorResponse
from models.datastore_info import DatastoreInfoParams, DatastoreInfoResponse
from models.datastore_search import DatastoreSearchParams, DatastoreSearchResponse
from models.datastore_search_sql import DatastoreSearchSqlParams, DatastoreSearchSqlResponse

DIST = Path("dist")

ERROR_RESPONSE_SCHEMA = TypeAdapter(ErrorResponse).json_schema()

BASE_URL = "https://data.humdata.org/api/3/action"

CKAN_ACTION_NOTE = (
    "CKAN actions accept parameters as either query string parameters (GET) "
    "or a JSON body (POST). Both methods are equivalent. "
    "All requests must include the `Authorization` header when accessing private resources."
)


def _schema(model) -> dict:
    return model.model_json_schema()


def _ref(name: str) -> dict:
    return {"$ref": f"#/components/schemas/{name}"}


def _error_response(description: str) -> dict:
    return {
        "description": description,
        "content": {
            "application/json": {
                "schema": _ref("ErrorResponse")
            }
        },
    }


def _common_errors() -> dict:
    return {
        "403": _error_response("Forbidden — resource is private or the action is not permitted."),
        "404": _error_response("Not Found — the resource_id does not exist in the DataStore."),
        "429": _error_response("Too Many Requests — rate limit exceeded."),
        "500": _error_response("Internal Server Error — unexpected server-side failure."),
    }


def build_spec() -> dict:
    return {
        "openapi": "3.1.0",
        "info": {
            "title": "HDX CKAN DataStore API",
            "version": "2.11.4",
            "description": (
                "OpenAPI specification for the CKAN DataStore API as exposed by the "
                "Humanitarian Data Exchange (HDX). "
                "Covers the Tabular Data Endpoints (TDE): `datastore_search`, "
                "`datastore_search_sql`, and `datastore_info`.\n\n"
                f"{CKAN_ACTION_NOTE}\n\n"
                "> **Note:** This specification documents behavior as described in the "
                "[CKAN 2.11.4 documentation](https://docs.ckan.org/en/latest/maintaining/datastore.html). "
                "Some parameter interactions (e.g. `filters` vs `q` in `datastore_search`) "
                "have nuanced behavior that is not fully captured here."
            ),
            "contact": {
                "name": "HDX Team",
                "url": "https://data.humdata.org",
            },
            "license": {
                "name": "Creative Commons Attribution International",
                "url": "https://creativecommons.org/licenses/by/4.0/",
            },
        },
        "servers": [
            {
                "url": BASE_URL,
                "description": "HDX Production",
            }
        ],
        "paths": {
            "/datastore_search": _datastore_search_path(),
            "/datastore_search_sql": _datastore_search_sql_path(),
            "/datastore_info": _datastore_info_path(),
        },
        "components": {
            "schemas": _collect_schemas(),
            "securitySchemes": {
                "ApiKeyAuth": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "Authorization",
                    "description": "CKAN API key. Required for all DataStore requests on HDX, including public resources.",
                }
            },
        },
        "security": [{"ApiKeyAuth": []}],
    }


def _datastore_search_path() -> dict:
    return {
        "get": {
            "operationId": "datastore_search_get",
            "summary": "Search a DataStore resource",
            "description": (
                "Query rows from a DataStore resource with optional filtering, full-text search, "
                "sorting, and pagination.\n\n"
                "Pass parameters as query string arguments (GET) or as a JSON body (POST)."
            ),
            "tags": ["DataStore"],
            "parameters": _params_from_model(DatastoreSearchParams),
            "responses": {
                "200": {
                    "description": "Successful response.",
                    "content": {
                        "application/json": {
                            "schema": _ref("DatastoreSearchResponse")
                        }
                    },
                },
                **_common_errors(),
            },
        },
        "post": {
            "operationId": "datastore_search_post",
            "summary": "Search a DataStore resource (POST)",
            "description": (
                "Identical to the GET form. Use POST to pass parameters as a JSON body, "
                "which is useful for large `filters` or `fields` payloads."
            ),
            "tags": ["DataStore"],
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": _ref("DatastoreSearchParams")
                    }
                },
            },
            "responses": {
                "200": {
                    "description": "Successful response.",
                    "content": {
                        "application/json": {
                            "schema": _ref("DatastoreSearchResponse")
                        }
                    },
                },
                **_common_errors(),
            },
        },
    }


def _datastore_search_sql_path() -> dict:
    return {
        "get": {
            "operationId": "datastore_search_sql_get",
            "summary": "Query a DataStore resource with SQL",
            "description": (
                "Execute a SQL `SELECT` statement against one or more DataStore resources. "
                "Useful for aggregations, joins, and complex filtering that `datastore_search` "
                "cannot express.\n\n"
                "Only `SELECT` statements are permitted."
            ),
            "tags": ["DataStore"],
            "parameters": _params_from_model(DatastoreSearchSqlParams),
            "responses": {
                "200": {
                    "description": "Successful response.",
                    "content": {
                        "application/json": {
                            "schema": _ref("DatastoreSearchSqlResponse")
                        }
                    },
                },
                **_common_errors(),
            },
        },
        "post": {
            "operationId": "datastore_search_sql_post",
            "summary": "Query a DataStore resource with SQL (POST)",
            "description": "Identical to the GET form. Use POST for long SQL statements.",
            "tags": ["DataStore"],
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": _ref("DatastoreSearchSqlParams")
                    }
                },
            },
            "responses": {
                "200": {
                    "description": "Successful response.",
                    "content": {
                        "application/json": {
                            "schema": _ref("DatastoreSearchSqlResponse")
                        }
                    },
                },
                **_common_errors(),
            },
        },
    }


def _datastore_info_path() -> dict:
    return {
        "get": {
            "operationId": "datastore_info_get",
            "summary": "Get DataStore resource metadata",
            "description": (
                "Retrieve field definitions, type information, and optional size/count metadata "
                "for a DataStore resource."
            ),
            "tags": ["DataStore"],
            "parameters": _params_from_model(DatastoreInfoParams),
            "responses": {
                "200": {
                    "description": "Successful response.",
                    "content": {
                        "application/json": {
                            "schema": _ref("DatastoreInfoResponse")
                        }
                    },
                },
                **_common_errors(),
            },
        },
        "post": {
            "operationId": "datastore_info_post",
            "summary": "Get DataStore resource metadata (POST)",
            "description": "Identical to the GET form.",
            "tags": ["DataStore"],
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": _ref("DatastoreInfoParams")
                    }
                },
            },
            "responses": {
                "200": {
                    "description": "Successful response.",
                    "content": {
                        "application/json": {
                            "schema": _ref("DatastoreInfoResponse")
                        }
                    },
                },
                **_common_errors(),
            },
        },
    }


def _params_from_model(model) -> list[dict]:
    schema = model.model_json_schema()
    required = set(schema.get("required", []))
    params = []
    for name, prop in schema.get("properties", {}).items():
        param: dict = {
            "name": name,
            "in": "query",
            "required": name in required,
            "schema": {k: v for k, v in prop.items() if k != "description"},
        }
        if "description" in prop:
            param["description"] = prop["description"]
        params.append(param)
    return params


def _collect_schemas() -> dict:
    schemas: dict = {}

    for model in [
        DatastoreSearchParams,
        DatastoreSearchResponse,
        DatastoreSearchSqlParams,
        DatastoreSearchSqlResponse,
        DatastoreInfoParams,
        DatastoreInfoResponse,
        ErrorResponse,
    ]:
        name = model.__name__
        schema = model.model_json_schema()
        if "$defs" in schema:
            for def_name, def_schema in schema.pop("$defs").items():
                schemas[def_name] = def_schema
        schemas[name] = schema

    # Rewrite all $ref values from #/$defs/Foo → #/components/schemas/Foo
    fixed = json.dumps(schemas).replace("#/$defs/", "#/components/schemas/")
    return json.loads(fixed)


def main():
    DIST.mkdir(exist_ok=True)
    spec = build_spec()
    out = DIST / "openapi.json"
    out.write_text(json.dumps(spec, indent=2))
    print(f"✓ Wrote {out} ({out.stat().st_size // 1024} KB)")
    print(f"  Endpoints: {len(spec['paths'])}")
    print(f"  Schemas:   {len(spec['components']['schemas'])}")


if __name__ == "__main__":
    sys.exit(main())
