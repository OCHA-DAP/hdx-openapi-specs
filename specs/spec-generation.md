# Spec Generation

> **Prefix:** `SPEC_GENERATION` — never reuse or renumber an ID.

## Summary

How `generate.py` assembles the OpenAPI 3.1 document from the Pydantic v2
models and writes it to `dist/openapi.json`.

## Scope

- Source-of-truth rules, document-level metadata, path/parameter/schema
  assembly, shared error responses, and output.

### Out of scope

- Undocumented or experimental CKAN parameters.
- Discrepancies between documented and observed CKAN behaviour (e.g. `filters` vs `q`),
  except HDX deviations recorded in `HDX_EDGE_CASES.md`.
- DataStore write actions.

## Requirements

Status: `[x]` implemented, `[ ]` planned / not yet implemented.

- [x] **SPEC_GENERATION-001** — The Pydantic v2 models in `models/` are the single source of truth; `python generate.py` builds `dist/openapi.json` from them, and the JSON is never hand-edited. No web framework is used.
- [x] **SPEC_GENERATION-002** — The output is a valid OpenAPI 3.1 document for "HDX APIs" (version `2.11.4`, CC BY 4.0), served from `https://data.humdata.org/api/3/action`, documenting exactly `datastore_search`, `datastore_search_sql`, `datastore_info`, and `package_search`.
- [x] **SPEC_GENERATION-003** — The API description introduces the Tabular Data Endpoints and catalog search, states that GET and POST are equivalent, and notes that the spec follows the CKAN 2.11 documentation.
- [x] **SPEC_GENERATION-004** — GET query parameters are generated from each `*Params` model, with `required` flags and descriptions taken from the model. All models are emitted under `components.schemas`, with nested definitions lifted and their references rewritten to match.
- [x] **SPEC_GENERATION-005** — Every successful response wraps the action's `result` in CKAN's `help` / `success` envelope.
- [x] **SPEC_GENERATION-006** — Every operation documents 403, 404, 409 (CKAN Validation Error), 429, and 500 responses using a shared `ErrorResponse` schema (`success: false`, `error.__type`, plus `message` or structured validation details).
- [x] **SPEC_GENERATION-007** — Every operation sets `x-hideTryItPanel: true` to hide GitBook's in-page "Test it" panel, which can't work for this API.

## Notes / open questions

- **No unit tests exist.** AGENTS.md requires all code to be covered by unit
  tests in `tests/`, but the repo has no `tests/` directory. Every `[x]`
  requirement above is currently unverified by tests; CI only checks that the
  output is a valid OpenAPI document.
