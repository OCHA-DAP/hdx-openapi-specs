# HDX APIs

An OpenAPI 3.1 specification for the [CKAN DataStore API](https://docs.ckan.org/en/2.11/maintaining/datastore.html), generated from Pydantic v2 models.

Covers endpoints exposed by [HDX](https://data.humdata.org):

| Endpoint | Tag | Description |
|---|---|---|
| `datastore_search` | DataStore | Filter, search, and paginate rows in a resource |
| `datastore_search_sql` | DataStore | Query one or more resources with SQL |
| `datastore_info` | DataStore | Retrieve field definitions and resource metadata |
| `package_search` | Catalog | Search for datasets |

---

## How it works

Parameters and response shapes are defined as **Pydantic v2 models** in `models/`. A small script (`generate.py`) calls `model_json_schema()` on each model and assembles a valid OpenAPI 3.1 object, writing it to `dist/openapi.json`.

No web framework is used — the Pydantic models are the single source of truth.

```
models/
  common.py               # Shared types (ErrorResponse)
  datastore_search.py     # Params + response models
  datastore_search_sql.py
  datastore_info.py
  package_search.py
generate.py               # Assembles and writes dist/openapi.json
```

---

## Generate locally

**Requirements:** Python 3.11+

```bash
pip install -e .
python generate.py
# → dist/openapi.json
```

To view the rendered spec, paste `dist/openapi.json` into [editor.swagger.io](https://editor.swagger.io).

---

## CI

On every push to `main`, the [GitHub Actions workflow](.github/workflows/generate.yml):

1. Installs dependencies
2. Runs `python generate.py`
3. Validates the generated spec against the OpenAPI 3.1 schema
4. Auto-commits `dist/openapi.json` if it changed
5. Deploys to GitHub Pages

---

## Updating the spec

All changes should be made to the Pydantic models in `models/`, not to the generated JSON directly. CI will regenerate and commit `dist/openapi.json` automatically on push to `main`.

---

## HDX-specific behaviour

HDX's deployment deviates from standard CKAN in several ways — most notably, authentication is required for all requests including public resources. See [HDX_EDGE_CASES.md](HDX_EDGE_CASES.md) before integrating.

---

## Scope and limitations

This specification documents behaviour as described in the CKAN 2.11 documentation. The following are out of scope:

- Undocumented or experimental parameters
- Discrepancies between documented and observed behaviour (e.g. subtle differences between `filters` and `q` in `datastore_search`)
- DataStore write actions (`datastore_create`, `datastore_upsert`, etc.)

---

## CKAN community contribution

The Pydantic models and generation script are structured to be reusable by any CKAN deployment. The models could be packaged independently, and the generation script could serve as a template for other CKAN operators. Any contribution should be framed as a starting point rather than a supported integration.
