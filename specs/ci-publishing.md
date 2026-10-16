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
- [x] **CI_PUBLISHING-002** — Every run regenerates the spec with Python 3.11 and validates it with `openapi-spec-validator`; an invalid spec fails the run.
- [x] **CI_PUBLISHING-003** — On `main` only, the validated spec is published to GitBook as `hdx-tde`, using the `GITBOOK_TOKEN` and `GITBOOK_ORG_ID` secrets; the step fails if the org ID is empty.
- [x] **CI_PUBLISHING-004** — A regenerated `dist/openapi.json` is committed back automatically (`chore: regenerate openapi.json`) only when it changed.
- [x] **CI_PUBLISHING-005** — On `main` only, `dist/` is deployed to GitHub Pages. Pull-request runs never publish to GitBook or deploy.

## Notes / open questions

- **README is incomplete.** The README's CI section omits the GitBook publish
  step and doesn't mention that PRs to `main` run generate + validate only.
- **Auto-commit on PR runs (unverified).** The auto-commit step has no
  `main`-only guard, so it also runs on pull-request runs. Needs checking:
  the auto-commit action may fail on a PR checkout (detached merge ref) if
  `dist/openapi.json` changed.
