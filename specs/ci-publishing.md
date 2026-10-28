# CI and Publishing

> **Prefix:** `CI_PUBLISHING` — never reuse or renumber an ID.

## Summary

The GitHub Actions workflow that regenerates, validates, commits, and
publishes the OpenAPI spec to GitBook and GitHub Pages.

## Scope

- Workflow triggers, permissions, generation/validation steps, and publishing targets.

### Out of scope

- GitBook site configuration beyond the spec upload.

## Requirements

Status: `[x]` implemented, `[ ]` planned / not yet implemented.

- [x] **CI_PUBLISHING-001** — The workflow runs on pushes and pull requests to `main` and on manual dispatch, with read-only token permissions by default; jobs request only the extra permissions they need.
- [x] **CI_PUBLISHING-002** — Every run regenerates the spec with Python 3.11 and validates it with `openapi-spec-validator` in a read-only `generate` job; an invalid spec fails the run. This is the only job that runs on pull requests.
- [x] **CI_PUBLISHING-003** — On `main` only, the validated spec is published to GitBook as `hdx-tde`, using the `GITBOOK_TOKEN` and `GITBOOK_ORG_ID` secrets; the step fails if the org ID is empty.
- [x] **CI_PUBLISHING-004** — On `main` only, a regenerated `dist/openapi.json` is committed back automatically (`chore: regenerate openapi.json`) only when it changed.
- [x] **CI_PUBLISHING-005** — On `main` only, `dist/` is deployed to GitHub Pages. Pull-request runs never publish to GitBook or deploy.
- [x] **CI_PUBLISHING-006** — Publishing (GitBook publish, auto-commit, Pages artifact upload) runs in a separate `publish` job on `main` only. It starts only after `generate` succeeds and publishes exactly the file `generate` validated, without regenerating it.
- [x] **CI_PUBLISHING-007** — The GitHub Pages site renders `openapi.json` with Redoc through `dist/index.html`, loading Redoc's `latest` standalone bundle as an ES module (`<script type="module">`). Fixes a blank Pages site: the `latest` bundle updated on 2026-10-14 uses `import.meta`, so loading it as a classic script failed with `Cannot use 'import.meta' outside a module` and Redoc never rendered.

## Notes / open questions

- **README is incomplete.** The README's CI section omits the GitBook publish
  step and doesn't mention that PRs to `main` run generate + validate only.
- **Unpinned Redoc (CI_PUBLISHING-007).** Loading `latest` means a new Redoc
  release can break the Pages site with no change in this repo, and CI won't
  notice — it validates `openapi.json` but never renders the page.