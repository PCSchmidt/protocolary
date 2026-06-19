# Protocolary Rename Checklist

**Started:** June 19, 2026
**Former working name:** Transcelerate
**New brand:** Protocolary
**Domain:** [protocolary.com](https://protocolary.com)

## Completed Locally

- [x] Adopt canonical brand and product naming
- [x] Add `BRAND_IDENTITY.md`
- [x] Add architecture Decision 011
- [x] Rename active documentation headings and product references
- [x] Rename the Python distribution to `protocolary-core`
- [x] Rename the FastAPI title to `Protocolary Clinical Study Compiler`
- [x] Rename development and test database defaults
- [x] Rename Docker Compose project to `protocolary`
- [x] Rename generated fixture system metadata
- [x] Rename session-start hook banners
- [x] Update the local ignored `.env` database names
- [x] Preserve TransCelerate BioPharma attribution, DDF references, and source URLs
- [x] Regenerate the competitive strategy PDF
- [x] Run the complete automated test suite

## Repository Preparation

- [x] Review the rename diff
- [x] Commit the Markdown, PDF, Word, brand, code, and configuration changes
- [x] Push the current `dev` branch
- [x] Confirm the repository does not depend on the old URL for active GitHub Actions

## GitHub Repository Rename — Completed

Completed June 19, 2026:

- [x] Renamed `PCSchmidt/transcelerate` to `PCSchmidt/protocolary`
- [x] Updated `origin` to `https://github.com/PCSchmidt/protocolary.git`
- [x] Verified the `dev` branch at the new URL
- [x] Verified GitHub's redirect from the former URL
- [x] Updated the repository description and homepage

Do not create a new repository at the old name; preserve GitHub's redirect.

## Local Folder Rename

The repository folder has been renamed:

```text
C:\Users\pchri\Documents\Transcelerate\protocolary
```

The outer workspace folder remains open by the current Codex session. After closing this
workspace, rename:

```text
C:\Users\pchri\Documents\Transcelerate
→ C:\Users\pchri\Documents\Protocolary
```

Then reopen the workspace at `C:\Users\pchri\Documents\Protocolary\protocolary`. The Docker
Compose project already uses the explicit name `protocolary`, so container naming no longer
depends on the folder name.

## Commercial Follow-up

- [ ] Perform a formal trademark search
- [ ] Decide whether to form a legal entity under the Protocolary name
- [ ] Configure a minimal landing page at `protocolary.com`
- [ ] Configure branded email when needed
- [ ] Reserve relevant GitHub organization and social identities
- [ ] Define logo, color, typography, and voice only after positioning interviews
- [ ] Update résumé, portfolio, LinkedIn, and demo materials after the public repository rename

Domain ownership establishes control of the web address but does not provide trademark clearance.
