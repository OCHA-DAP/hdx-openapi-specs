# DataStore (Tabular Data Endpoints)

> **Prefix:** `DATASTORE` — never reuse or renumber an ID.

## Summary

The OpenAPI description of the read-only CKAN DataStore actions that HDX
exposes as its Tabular Data Endpoints (TDE): `datastore_search`,
`datastore_search_sql`, and `datastore_info`.

## Scope

- Request parameters, response shapes, and operation metadata for the three
  DataStore read actions.

### Out of scope

- DataStore write actions (`datastore_create`, `datastore_upsert`, `datastore_delete`, …).
- Undocumented or experimental CKAN parameters.
- Authentication — see [authentication.md](authentication.md).
- Shared error responses — see [spec-generation.md](spec-generation.md).

## Requirements

Status: `[x]` implemented, `[ ]` planned / not yet implemented.

- [x] **DATASTORE-001** — `datastore_search`, `datastore_search_sql`, and `datastore_info` are each exposed as a GET (query-string parameters) and a POST (JSON body) operation, tagged `DataStore` and documented as equivalent.

### `datastore_search`

- [x] **DATASTORE-002** — Requires `resource_id` (id or alias). Rows can be narrowed by `filters` (exact `{field: value}` match on all conditions) and/or full-text search via `q` (a string, or `{field: query}`) or `full_text`, tuned by `plain` (default `true`; `false` enables tsquery syntax) and `language` (default `english`).
- [x] **DATASTORE-003** — Output can be shaped with `fields` (list or comma-separated string), `sort` (`"field asc, field2 desc"`), `distinct`, `limit` (default `100`), `offset`, and `records_format` (`objects` | `lists` | `csv` | `tsv`, default `objects`); `records` takes the matching shape.
- [x] **DATASTORE-004** — `include_total` (default `true`) returns a `total` row count; above `total_estimation_threshold` the total may be estimated, flagged by `total_was_estimated`.
- [x] **DATASTORE-005** — The response always includes field descriptors and `_links` with `start` and `next` pagination URLs.

### `datastore_search_sql`

- [x] **DATASTORE-006** — Requires `sql`: a single `SELECT` statement with resource IDs as table names; other statements are not allowed. The response returns field descriptors and row objects, with `records_truncated` set when the server's 32,000-row limit is hit.

### `datastore_info`

- [x] **DATASTORE-007** — Requires `resource_id` (id or alias). Returns field descriptors and optional `meta` with aliases, row count, table/index/database sizes, and `table_type` (`BASE TABLE` | `VIEW` | `FOREIGN` | `LOCAL TEMPORARY`).

## Notes / open questions

- `models/common.py` defines a `FieldInfo` model (`id`, `type`, `info`), but
  response `fields` are typed as `list[dict]` and `FieldInfo` is not referenced
  by any response model or emitted into `components.schemas`.
