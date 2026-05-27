# Changelog

## v1.0.0-prod — 2026-05-27

- Production hardening pass: confirmed the GitHub Actions Pages workflow runs green (pytest + smoke_check + site generation) at HEAD before tagging v1.0-prod.
- Added `LICENSE` (AGPL-3.0-or-later) and `CODE_OF_CONDUCT.md` to align with the Kinetic Gain Suite governance baseline.
- Added `.github/dependabot.yml` with weekly pip + github-actions update schedules.
- No `src/`, README narrative, docs, or screenshot edits — squad doctrine respects the v0.1-shipped surface.

## v0.1-shipped

- initial public release of the regulatory reporting mart
- shipped executable SQL marts for readiness and deadline pressure
- published a static operator surface at `reporting.kineticgain.com`
