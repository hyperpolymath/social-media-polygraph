<!--
SPDX-License-Identifier: MPL-2.0
SPDX-FileCopyrightText: 2026 Jonathan D.A. Jewell (hyperpolymath)
-->

# Changelog

All notable changes to `social-media-polygraph` will be documented in this file.

This file is generated from conventional commits by the
[`changelog-reusable.yml`](https://github.com/hyperpolymath/standards/blob/main/.github/workflows/changelog-reusable.yml)
workflow (`hyperpolymath/standards#206`). Adopt the workflow in this repo's CI to keep this file in sync automatically — see
[`templates/cliff.toml`](https://github.com/hyperpolymath/standards/blob/main/templates/cliff.toml)
for the canonical config.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
this project aims to follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- feat: import foundation from social-media-tools/polygraph fork

### Fixed

- fix(ci): sync hypatia-scan.yml to canonical (kill cd-scanner build drift) (#15)
- fix(ci): build Hypatia escript from repo root (estate dogfood drift)
- fix(ci): rsr-antipattern.yml duplicate heredoc (#14)

### Documentation

- docs: record tech-debt audit findings (2026-05-26) (#26)
- docs(readme): add SPDX header, OSSF and GWF badges; fix license badge to PMPL

### CI

- ci: bump actions/upload-artifact SHA to current v4 (#13)
- ci(antipattern): fix top-level dir matching + benchmarks/lsp/bench filename allowlists (#9)
- ci(antipattern): TS check reads .claude/CLAUDE.md exemption table (#8)
- ci(antipattern): broaden TS allowlist (cli/, mod.ts, lsp-server, *vscode*, deno-*) (#7)
- ci(antipattern): allowlist legit TS bridge/adapter paths (#6)

## Pre-history

Prior commits to this file's introduction are recorded in git history but not formally classified into Keep-a-Changelog sections. To backfill, run `git cliff -o CHANGELOG.md` locally using the canonical [`cliff.toml`](https://github.com/hyperpolymath/standards/blob/main/templates/cliff.toml) — this is one-shot mechanical work.

---

<!-- This file was seeded by the 2026-05-26 estate tech-debt audit follow-up (Row-2 Phase 3); see [`hyperpolymath/standards/docs/audits/2026-05-26-estate-documentation-debt.md`](https://github.com/hyperpolymath/standards/blob/main/docs/audits/2026-05-26-estate-documentation-debt.md). -->
