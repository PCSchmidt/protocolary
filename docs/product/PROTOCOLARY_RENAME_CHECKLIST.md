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

## Complete Before the Repository Rename

- [ ] Review the rename diff
- [ ] Commit the Markdown, PDF, Word, brand, code, and configuration changes
- [ ] Push the current `dev` branch
- [ ] Confirm GitHub Actions and external links do not depend on the old repository URL

## GitHub Repository Rename

1. Rename `PCSchmidt/transcelerate` to `PCSchmidt/protocolary` in GitHub repository settings.
2. Update the local remote:

   ```bash
   git remote set-url origin https://github.com/PCSchmidt/protocolary.git
   git remote -v
   git fetch origin
   git push
   ```

3. Update the repository description and website:

   ```text
   Protocolary Build: governed USDM-to-EDC clinical study automation
   https://protocolary.com
   ```

4. Do not create a new repository at the old name; preserve GitHub's redirect.

## Local Folder Rename

After the GitHub rename and a clean working tree, optionally rename:

```text
C:\Users\pchri\Documents\Transcelerate\transcelerate
```

to:

```text
C:\Users\pchri\Documents\Protocolary\protocolary
```

Then reopen the workspace from the new path. The Docker Compose project already uses the explicit
name `protocolary`, so container naming no longer depends on the folder name.

## Commercial Follow-up

- [ ] Perform a formal trademark search
- [ ] Decide whether to form a legal entity under the Protocolary name
- [ ] Configure a minimal landing page at `protocolary.com`
- [ ] Configure branded email when needed
- [ ] Reserve relevant GitHub organization and social identities
- [ ] Define logo, color, typography, and voice only after positioning interviews
- [ ] Update résumé, portfolio, LinkedIn, and demo materials after the public repository rename

Domain ownership establishes control of the web address but does not provide trademark clearance.
