from typing import Any, Literal
from pydantic import BaseModel, Field


class DatastoreInfoParams(BaseModel):
    resource_id: str = Field(
        ...,
        description="The `id` or alias of the DataStore resource to describe. Required.",
    )
    include_meta: bool | None = Field(
        True,
        description=(
            "Include size metrics and row count in the response "
            "(`count`, `db_size`, `idx_size`, `size`). Defaults to `true`."
        ),
    )
    include_fields_schema: bool | None = Field(
        True,
        description=(
            "Include field index and uniqueness properties in each field descriptor. "
            "Defaults to `true`."
        ),
    )


class DatastoreResourceMeta(BaseModel):
    aliases: list[str] = Field(..., description="List of aliases defined for this resource.")
    count: int | None = Field(None, description="Total number of rows in the resource table.")
    db_size: int | None = Field(None, description="Total size of the database in bytes.")
    id: str = Field(..., description="The resource ID.")
    idx_size: int | None = Field(None, description="Size of indexes on this resource table in bytes.")
    size: int | None = Field(None, description="Size of this resource table in bytes.")
    table_type: Literal["BASE TABLE", "VIEW", "FOREIGN", "LOCAL TEMPORARY"] | None = Field(
        None,
        description="PostgreSQL table type for this resource.",
    )


class DatastoreInfoResponse(BaseModel):
    help: str = Field(..., description="URL to the API documentation for this action.")
    success: bool = Field(..., description="Whether the request succeeded.")
    result: "DatastoreInfoResult"


class DatastoreInfoResult(BaseModel):
    meta: DatastoreResourceMeta | None = Field(
        None,
        description="Resource metadata. Present when `include_meta` is `true`.",
    )
    fields: list[dict[str, Any]] = Field(
        ...,
        description=(
            "List of field descriptor objects. Each contains `id`, `type`, and optionally "
            "`schema` (with index and uniqueness info when `include_fields_schema` is `true`)."
        ),
    )
