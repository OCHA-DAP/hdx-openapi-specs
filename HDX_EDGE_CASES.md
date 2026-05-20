# HDX CKAN DataStore — Edge Cases and Deviations from Standard CKAN

This document records known differences between HDX's deployment of the CKAN DataStore API and the upstream CKAN 2.11.4 documentation. It is intended to keep the OpenAPI spec accurate and to help developers avoid integration pitfalls.

---

## Authentication

**Standard CKAN behaviour:** Authentication is required only for private resources. Public resources can be queried anonymously.

**HDX behaviour:** Authentication is required for **all** DataStore requests, including public resources. Unauthenticated requests return:

```json
{
  "error": {
    "__type": "Authorization Error",
    "message": "Access denied: Action datastore_search requires an authenticated user"
  },
  "success": false
}
```

**How to authenticate:** Pass your HDX API key in the `Authorization` header:

```bash
curl -H "Authorization: <your-api-key>" \
  "https://data.humdata.org/api/action/datastore_search?resource_id=<id>&limit=5"
```

Your API key is available at `data.humdata.org` → profile → API key.

---

## Unsupported parameters

The following parameters appear in the CKAN 2.11.4 documentation but are **not supported** by HDX's deployment. Passing them returns a validation error:

| Parameter | Endpoint | Error |
|---|---|---|
| `include_next_page` | `datastore_search` | `invalid value "include_next_page"` |

Example error response:

```json
{
  "error": {
    "__extras": ["invalid value \"include_next_page\""],
    "__type": "Validation Error"
  },
  "success": false
}
```

These parameters have been omitted from the OpenAPI spec.

---

## CORS

HDX's API does not return `Access-Control-Allow-Origin` headers that permit cross-origin browser requests from arbitrary domains. This means:

- **Swagger UI / editor.swagger.io "Try it out"** will fail with a CORS error — the browser blocks the request before it reaches HDX.
- **Server-side calls** (curl, Python, GitHub Actions) are unaffected.

For interactive testing, use curl or a local script rather than a browser-based tool.

---

## datastore_info: ignored parameters

The following `datastore_info` parameters are documented in CKAN 2.11.4 but are **silently ignored** by HDX — the full response is returned regardless of their value:

| Parameter | Documented behaviour | HDX behaviour |
|---|---|---|
| `include_meta` | `false` omits the `meta` block | `meta` always returned |
| `include_fields_schema` | `false` omits `schema` from each field | `schema` always returned |

These parameters remain in the spec for completeness against the CKAN documentation, but developers integrating with HDX should not rely on them to reduce response size.

---

## SQL injection protection

`datastore_search_sql` does not permit non-`SELECT` statements. Attempts to run `DROP`, `INSERT`, `UPDATE`, or DDL are rejected with a `Validation Error`. Note: CKAN wraps the submitted SQL in an outer `SELECT * FROM (...) LIMIT` wrapper before execution, so the error manifests as a PostgreSQL syntax error rather than an explicit permission denial.

---

## Spec scope reminder

Per the [project proposal](README.md), this spec documents behaviour **as described in the CKAN documentation**, not as observed in production. The exceptions above are documented here because they affect usability for HDX integrators specifically, not because they represent general CKAN behaviour.

Additional observed-vs-documented discrepancies (e.g. subtle differences between `filters` and `q`) are out of scope and not captured here.
