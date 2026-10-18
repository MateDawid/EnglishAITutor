# ADR 0001: Architecture documentation format

- Status: Accepted
- Date: 2026-10-18

## Context

The repository needs architecture information that is easy for both contributors and coding agents to read, review, and update alongside source changes. Repository-specific agent instructions should be discoverable without mixing them into a diagram or a general architecture description.

## Decision

- Keep concise, repository-wide agent guidance in the root `AGENTS.md`.
- Describe the implemented system and its Mermaid diagrams in `docs/architecture.md`.
- Record significant accepted architecture decisions as numbered ADRs in `docs/decisions/`.
- Use Markdown and Mermaid as the version-controlled source; do not make a binary diagram file the authoritative architecture description.

## Consequences

- Architecture and agent guidance can be reviewed in ordinary code diffs and updated with implementation changes.
- Mermaid diagrams are textual and may be rendered by compatible Markdown viewers.
- These documents must describe current behavior accurately; proposed or future functionality must be labeled as such.
