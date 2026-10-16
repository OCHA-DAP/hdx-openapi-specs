# Authentication

> **Prefix:** `AUTHENTICATION` — never reuse or renumber an ID.

## Summary

How the OpenAPI spec describes authentication for HDX APIs, including HDX's
deviation from standard CKAN: DataStore requests require a token even for
public resources.

## Scope

- Security schemes and per-operation security requirements.
- Documentation of authentication-related errors and permission-gated parameters.

### Out of scope

- Token issuance and management (handled in the HDX web UI).

## Requirements

Status: `[x]` implemented, `[ ]` planned / not yet implemented.

- [x] **AUTHENTICATION-001** — Every DataStore operation requires an HDX API token in the `Authorization` header (`ApiKeyAuth` scheme), even for public resources — an HDX deviation from standard CKAN. A missing or invalid token returns 403.
- [x] **AUTHENTICATION-002** — Catalog operations accept requests with or without a token, using a separate `ApiKeyAuthCatalog` scheme (same header) so the docs can describe the token as optional.
- [x] **AUTHENTICATION-003** — `package_search` documents that `include_private` requires membership of the owning organisation and `include_drafts` requires being the owning user or an org admin.

## Notes / open questions

- None.
