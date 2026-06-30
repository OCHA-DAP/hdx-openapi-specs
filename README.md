# CKAN DataStore OpenAPI Specification

An OpenAPI 3.1 specification for the [CKAN DataStore API](https://docs.ckan.org/en/latest/maintaining/datastore.html), generated from Pydantic v2 models.

Covers the three Tabular Data Endpoints (TDE) exposed by [HDX](https://data.humdata.org):

| Endpoint | Description |
|---|---|
| `datastore_search` | Filter, search, and paginate rows in a resource |
| `datastore_search_sql` | Query one or more resources with SQL |
| `datastore_info` | Retrieve field definitions and resource metadata |

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

To test against the live API, set your HDX API key (available from your profile on data.humdata.org):

```bash
HDX_API_KEY=<your-key> bash test.sh
```

---

## CI

On every push to `main`, the [GitHub Actions workflow](.github/workflows/generate.yml):

1. Installs dependencies
2. Runs `python generate.py`
3. Uploads `dist/openapi.json` as a downloadable artifact

The generated spec is available under the **Actions** tab → latest run → **Artifacts**.

---

## Updating the spec

All changes should be made to the Pydantic models in `models/`, not to the generated JSON directly. Re-run `python generate.py` to regenerate.

---

## HDX-specific behaviour

HDX's deployment deviates from standard CKAN in several ways — authentication requirements, unsupported parameters, and CORS restrictions. See [HDX_EDGE_CASES.md](HDX_EDGE_CASES.md) before integrating.

---

## Testing

See [TESTING.md](TESTING.md) for the full test record (36 tests across all endpoints, parameters, HTTP methods, and error cases).

---

## Scope and limitations

This specification documents behaviour as described in the CKAN 2.11.4 documentation. The following are out of scope:

- Undocumented or experimental parameters
- Discrepancies between documented and observed behaviour (e.g. subtle differences between `filters` and `q` in `datastore_search`)
- DataStore write actions (`datastore_create`, `datastore_upsert`, etc.)

---

## CKAN community contribution

The Pydantic models and generation script are structured to be reusable by any CKAN deployment. The models could be packaged independently, and the generation script could serve as a template for other CKAN operators. Any contribution should be framed as a starting point rather than a supported integration.
