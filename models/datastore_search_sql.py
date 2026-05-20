from typing import Any
from pydantic import BaseModel, Field


class DatastoreSearchSqlParams(BaseModel):
    sql: str = Field(
        ...,
        description=(
            "A single SQL `SELECT` statement to execute against the DataStore. Required. "
            "Only `SELECT` statements are permitted — `INSERT`, `UPDATE`, `DELETE`, and DDL "
            "statements are not allowed. "
            "Table names correspond to resource IDs (e.g. `SELECT * FROM \"<resource_id>\"`)."
        ),
    )


class DatastoreSearchSqlResponse(BaseModel):
    help: str = Field(..., description="URL to the API documentation for this action.")
    success: bool = Field(..., description="Whether the request succeeded.")
    result: "DatastoreSearchSqlResult"


class DatastoreSearchSqlResult(BaseModel):
    sql: str = Field(
        ...,
        description="The SQL query echoed back from the request.",
    )
    fields: list[dict[str, Any]] = Field(
        ...,
        description="List of field descriptor objects for the result columns, each with `id` and `type` keys.",
    )
    records: list[dict[str, Any]] = Field(
        ...,
        description="List of result row objects.",
    )
    records_truncated: bool | None = Field(
        None,
        description="Present and `true` if the result set was truncated due to a server-side row limit.",
    )
