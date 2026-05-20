# API Testing Record

Tests run against the live HDX DataStore API (`https://data.humdata.org/api/3/action`) using resource `e3a18c4c-ec1b-457e-9f60-cee283c04e0c` (HDX HAPI Operational Presence, public dataset).

All 36 tests pass.

---

## datastore_search (20 tests)

### Core behaviour
| Test | Result |
|---|---|
| Returns `success: true` | PASS |
| `limit=5` returns exactly 5 records | PASS |
| `offset=1` shifts records (`_id` starts at 2) | PASS |
| `include_total=false` omits `total` from response | PASS |
| `_links` always present in response | PASS |
| `_links.next` contains correct `offset` increment | PASS |

### Parameters
| Test | Result |
|---|---|
| `fields` restricts columns in response | PASS |
| `fields` as comma-separated string | PASS |
| `sort=_id asc` returns ascending order | PASS |
| `sort=_id desc` returns descending order | PASS |
| `filters` with single condition returns matching rows | PASS |
| `filters` with two conditions returns matching rows | PASS |
| `q` full-text search returns results | PASS |
| `full_text` search returns results | PASS |
| `plain=false` tsquery syntax accepted | PASS |
| `distinct=true` returns unique rows | PASS |

### records_format
| Test | Result |
|---|---|
| `records_format=objects` (default) returns list of dicts | PASS |
| `records_format=lists` returns list of lists | PASS |
| `records_format=csv` returns string | PASS |
| `records_format=tsv` returns string | PASS |

---

## datastore_search_sql (5 tests)

| Test | Result |
|---|---|
| Basic `SELECT * LIMIT 1` returns success | PASS |
| SQL query echoed back in `result.sql` | PASS |
| `COUNT(*)` aggregate query works | PASS |
| `WHERE` clause filters rows correctly | PASS |
| Non-`SELECT` statement (`DROP TABLE`) is rejected | PASS |

---

## datastore_info (5 tests)

| Test | Result |
|---|---|
| Returns `success: true` | PASS |
| `meta` contains `id`, `count`, `table_type` | PASS |
| `fields` list is non-empty | PASS |
| `include_meta=false` — param accepted (ignored by HDX, see [HDX_EDGE_CASES.md](HDX_EDGE_CASES.md)) | PASS |
| `include_fields_schema=false` — param accepted (ignored by HDX, see [HDX_EDGE_CASES.md](HDX_EDGE_CASES.md)) | PASS |

---

## POST endpoints (3 tests)

All three endpoints accept JSON body via POST in addition to GET query params.

| Test | Result |
|---|---|
| `POST /datastore_search` with JSON body | PASS |
| `POST /datastore_search_sql` with JSON body | PASS |
| `POST /datastore_info` with JSON body | PASS |

---

## Error cases (3 tests)

| Test | Expected | Result |
|---|---|---|
| Unknown `resource_id` | `success: false`, Not Found Error | PASS |
| Request with no `Authorization` header | `success: false`, Authorization Error | PASS |
| `DROP TABLE` via `datastore_search_sql` | `success: false`, Validation Error | PASS |

---

## Known HDX deviations

See [HDX_EDGE_CASES.md](HDX_EDGE_CASES.md) for full details. Summary:

| Behaviour | CKAN docs | HDX |
|---|---|---|
| Auth required | Only for private resources | Always required |
| `include_next_page` param | Supported | Not supported (removed from spec) |
| `include_meta=false` | Omits meta block | Ignored, meta always returned |
| `include_fields_schema=false` | Omits schema from fields | Ignored, schema always returned |
| CORS | Varies | Not supported for browser requests |
