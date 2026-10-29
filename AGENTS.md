# Repository guidance

## Before making changes

- Inspect the relevant implementation and nearby tests before changing behavior.
- Read the relevant sections of [docs/architecture.md](docs/architecture.md) for architecture, API, data-model, or security changes. It describes a target design; check its current-state notes before treating a proposal as implemented.
- Check existing tests and follow the patterns in the affected feature.
- Keep architecture documentation aligned with implementation and label target designs or proposals clearly.

## Project structure

- `frontend/src`: React and TypeScript single-page application, organized by feature (`auth`, `chat`, `flashcards`) and shared `core`.
- `backend/src`: FastAPI application organized by feature (`auth`, `core`, `flashcards`) with shared database, configuration, filtering, pagination, and sorting utilities.
- `backend/src/alembic`: database migrations and flashcard seed data.
- `backend/tests` and `frontend/src`: backend and frontend tests.

## Validation

- Frontend: from `frontend/`, run `npm run build`, `npm run lint`, and focused tests with `npm run test:run -- <test-file>`.
- Backend: use the existing Docker Compose test setup in `backend/docker-compose-tests.yaml`. Run `ruff check .`, `ruff format --check .`, and focused pytest tests with `docker compose -f backend/docker-compose-tests.yaml run --rm -e ENV=local -e PGPASSWORD=tutor_password backend pytest <test-path>` from the repository root.
- For database/schema changes, review the Alembic migration and test both the affected database behavior and relevant API behavior.

## Architecture boundaries

- The frontend calls the backend through the shared Axios client in `frontend/src/core/apiClient.ts`.
- Current authentication uses OAuth2 bearer tokens: login returns a JWT in the response, the frontend stores it in `localStorage`, and requests send it in the `Authorization` header. Follow this implemented behavior unless explicitly changing the authentication design; the secure-cookie and CSRF flow in `docs/architecture.md` is a target design, not current behavior.
- Backend routes should use the existing feature routers, services, schemas, and async SQLAlchemy session dependency rather than accessing the database from frontend code.
- Record significant, accepted architectural decisions as numbered ADRs in `docs/decisions/`. Do not use ADRs to present unapproved proposals as implemented decisions.
- During implementation, if a significant cross-cutting architectural decision is needed, explain the options and trade-offs and ask whether to record the accepted choice as an ADR; skip routine implementation choices.
