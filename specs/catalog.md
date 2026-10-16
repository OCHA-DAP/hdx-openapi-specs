# Catalog Search

> **Prefix:** `CATALOG` — never reuse or renumber an ID.

## Summary

The OpenAPI description of HDX's catalog (metadata) search, CKAN's
`package_search` action, used to discover datasets.

## Scope

- Request parameters, response shape, and operation metadata for `package_search`.

### Out of scope

- Other CKAN catalog actions (`package_show`, `organization_list`, …).
- Authentication — see [authentication.md](authentication.md).
- Shared error responses — see [spec-generation.md](spec-generation.md).

## Requirements

Status: `[x]` implemented, `[ ]` planned / not yet implemented.

- [x] **CATALOG-001** — `package_search` is exposed as a GET (query-string parameters) and a POST (JSON body) operation, tagged `Catalog` and documented as equivalent.
- [x] **CATALOG-002** — Datasets are queried with Solr syntax: `q` (default `*:*`), filter queries `fq` and `fq_list` (ANDed together), `sort` (default `score desc, metadata_modified desc`), and pagination via `rows` (default `10`, max `1000`) and `start`.
- [x] **CATALOG-003** — Faceting is controlled by `facet` (default `"true"`) and the dotted Solr parameters `facet.mincount`, `facet.limit` (default `50`), and `facet.field`.
- [x] **CATALOG-004** — Drafts, deleted, and private datasets are excluded unless `include_drafts`, `include_deleted`, or `include_private` is set; `use_default_schema` switches to CKAN's default package schema.
- [x] **CATALOG-005** — The response returns the match `count`, the dataset `results`, and `search_facets`.
- [x] **CATALOG-006** — The 404 response means the action/endpoint does not exist, not a missing `resource_id` as on DataStore endpoints.

## Notes / open questions

- None.
