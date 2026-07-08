from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class PackageSearchParams(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    q: str | None = Field(
        "*:*",
        description='Solr search query. Supports Solr syntax. Defaults to `"*:*"` (all datasets).',
    )
    fq: str | None = Field(
        None,
        description="Solr filter query. Restricts results without affecting relevance scoring.",
    )
    fq_list: list[str] | None = Field(
        None,
        description="Additional filter queries as a list. Each entry is ANDed with `fq`.",
    )
    sort: str | None = Field(
        "score desc, metadata_modified desc",
        description='Sort order as a Solr sort string. Defaults to `"score desc, metadata_modified desc"`.',
    )
    rows: int | None = Field(
        10,
        ge=0,
        le=1000,
        description="Maximum number of datasets to return. Defaults to `10`, maximum `1000`.",
    )
    start: int | None = Field(
        None,
        ge=0,
        description="Offset into the result set. Used for pagination.",
    )
    facet: str | None = Field(
        "true",
        description='Enable faceted results. Defaults to `"true"`.',
    )
    facet_mincount: int | None = Field(
        None,
        alias="facet.mincount",
        description="Minimum count for a facet value to be included in the response.",
    )
    facet_limit: int | None = Field(
        50,
        alias="facet.limit",
        description="Maximum number of values returned per facet field. Defaults to `50`.",
    )
    facet_field: list[str] | None = Field(
        None,
        alias="facet.field",
        description="Fields to facet on.",
    )
    include_drafts: bool | None = Field(
        False,
        description="Include draft datasets in results. Requires authentication as the owning user or org admin. Defaults to `false`.",
    )
    include_deleted: bool | None = Field(
        False,
        description="Include deleted datasets in results. Defaults to `false`.",
    )
    include_private: bool | None = Field(
        False,
        description="Include private datasets in results. Requires authentication as a member of the owning organisation. Defaults to `false`.",
    )
    use_default_schema: bool | None = Field(
        False,
        description="Return results using the default package schema rather than any custom schema configured on the instance. Defaults to `false`.",
    )


class PackageSearchResult(BaseModel):
    count: int = Field(..., description="Total number of datasets matching the query.")
    results: list[dict[str, Any]] = Field(..., description="List of matching dataset objects.")
    sort: str | None = Field(None, description="Sort string echoed from the request.")
    facets: dict[str, Any] | None = Field(None, description="Legacy facet counts. Prefer `search_facets`.")
    search_facets: dict[str, Any] = Field(
        ...,
        description=(
            "Facet counts keyed by field name. Each entry has a `title` and an `items` list "
            "of `{name, display_name, count}` objects."
        ),
    )
    facet_pivot: dict[str, Any] | None = Field(None, description="Pivot facet results, if requested.")
    facet_queries: dict[str, Any] | None = Field(None, description="Facet query results, if requested.")
    expanded: dict[str, Any] | None = Field(None, description="Expanded results, if requested.")


class PackageSearchResponse(BaseModel):
    help: str = Field(..., description="URL to the API documentation for this action.")
    success: bool = Field(..., description="Whether the request succeeded.")
    result: PackageSearchResult
