from typing import Any, Literal
from pydantic import BaseModel, ConfigDict, Field


class DatastoreSearchParams(BaseModel):
    resource_id: str = Field(
        ...,
        description="The `id` or alias of the resource to search. Required.",
    )
    filters: dict[str, Any] | None = Field(
        None,
        description=(
            "Matching conditions as a dictionary of `{field: value}` pairs. "
            "Rows must match all conditions. Example: `{\"country\": \"Uganda\"}`."
        ),
    )
    q: str | dict[str, Any] | None = Field(
        None,
        description=(
            "Full-text search query. Pass a string to search across all fields, "
            "or a dictionary of `{field: query}` to target specific fields. "
            "Note: behavior differs subtly from `filters` — `q` uses full-text ranking "
            "while `filters` performs exact matching."
        ),
    )
    full_text: str | None = Field(
        None,
        description=(
            "Full-text search query applied across all fields. "
            "Similar to `q` with a string value, but always searches all fields. "
            "Cannot be combined with `q`."
        ),
    )
    distinct: bool | None = Field(
        False,
        description="Return only unique rows. Defaults to `false`.",
    )
    plain: bool | None = Field(
        True,
        description=(
            "Treat the `q` query as plain text (no special FTS operators). "
            "Set to `false` to use PostgreSQL tsquery syntax. Defaults to `true`."
        ),
    )
    language: str | None = Field(
        "english",
        description="Language used for full-text search stemming. Defaults to `english`.",
    )
    limit: int | None = Field(
        100,
        ge=0,
        description="Maximum number of rows to return. Defaults to `100`.",
    )
    offset: int | None = Field(
        None,
        ge=0,
        description="Number of rows to skip before returning results. Used for pagination.",
    )
    fields: list[str] | str | None = Field(
        None,
        description=(
            "Columns to include in the response. Pass a comma-separated string or a list. "
            "Defaults to all fields."
        ),
    )
    sort: str | None = Field(
        None,
        description=(
            "Comma-separated list of fields to sort by, with optional `asc`/`desc` direction. "
            "Example: `\"fieldname1 asc, fieldname2 desc\"`."
        ),
    )
    include_total: bool | None = Field(
        True,
        description="Include the total number of matching rows in the response. Defaults to `true`.",
    )
    records_format: Literal["objects", "lists", "csv", "tsv"] | None = Field(
        "objects",
        description=(
            "Format for the returned records. "
            "`objects` returns a list of dicts, "
            "`lists` returns a list of lists, "
            "`csv` and `tsv` return delimited strings. "
            "Defaults to `objects`."
        ),
    )


class DatastoreSearchResponse(BaseModel):
    help: str = Field(..., description="URL to the API documentation for this action.")
    success: bool = Field(..., description="Whether the request succeeded.")
    result: "DatastoreSearchResult"


class DatastoreSearchLinks(BaseModel):
    start: str = Field(..., description="URL to the first page of results with the same parameters.")
    next: str = Field(..., description="URL to the next page of results.")


class DatastoreSearchResult(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    resource_id: str = Field(..., description="The resource ID that was queried.")
    fields: list[dict[str, Any]] = Field(
        ...,
        description="List of field descriptor objects, each with `id` and `type` keys.",
    )
    offset: int | None = Field(None, description="The offset used in the query.")
    limit: int = Field(..., description="The limit used in the query.")
    filters: dict[str, Any] | None = Field(None, description="Filters applied to the query.")
    include_total: bool | None = Field(
        None,
        description="Echoed from the request parameter. Indicates whether `total` is included.",
    )
    records_format: str | None = Field(
        None,
        description="Echoed from the request parameter. Format used for `records`.",
    )
    total: int | None = Field(
        None,
        description="Total number of matching rows. Present when `include_total` is `true`.",
    )
    total_was_estimated: bool | None = Field(
        None,
        description="Whether the total count was estimated rather than exact.",
    )
    total_estimation_threshold: int | None = Field(
        None,
        description="Row count threshold above which total estimation is used. `null` when estimation is not configured.",
    )
    records: list[dict[str, Any]] | list[list[Any]] | str = Field(
        ...,
        description="Matching rows. Shape depends on `records_format`.",
    )
    links: DatastoreSearchLinks | None = Field(
        None,
        alias="_links",
        description="Pagination helper URLs. Always present — `next` contains the URL for the next page of results.",
    )
