# HDX CKAN DataStore — Edge Cases and Deviations from Standard CKAN

This document records known differences between HDX's deployment of the CKAN DataStore API and the upstream CKAN 2.11 documentation. It is intended to keep the OpenAPI spec accurate and to help developers avoid integration pitfalls.

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

## SQL injection protection

`datastore_search_sql` does not permit non-`SELECT` statements. Attempts to run `DROP`, `INSERT`, `UPDATE`, or DDL are rejected with a `Validation Error`. Note: CKAN wraps the submitted SQL in an outer `SELECT * FROM (...) LIMIT` wrapper before execution, so the error manifests as a PostgreSQL syntax error rather than an explicit permission denial.

---

## Spec scope reminder

Per the [project proposal](README.md), this spec documents behaviour **as described in the CKAN 2.11 documentation**, not as observed in production. The exceptions above are documented here because they affect usability for HDX integrators specifically, not because they represent general CKAN behaviour.

Additional observed-vs-documented discrepancies (e.g. subtle differences between `filters` and `q`) are out of scope and not captured here.
