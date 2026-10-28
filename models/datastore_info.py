from typing import Literal
from pydantic import BaseModel, Field

from models.common import FieldInfo


class DatastoreInfoParams(BaseModel):
    resource_id: str = Field(
        ...,
        description="The `id` or alias of the DataStore resource to describe. Required.",
    )


class DatastoreResourceMeta(BaseModel):
    aliases: list[str] = Field(..., description="List of aliases defined for this resource.")
    count: int | None = Field(None, description="Total number of rows in the resource table.")
    db_size: int | None = Field(None, description="Total size of the DataStore database in bytes (all tables, not just this resource).")
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
        description="Resource metadata including aliases, row count, and size information.",
    )
    fields: list[FieldInfo] = Field(
        ...,
        description="One descriptor per column: its name, CKAN type, and data dictionary entry (`info`).",
    )
