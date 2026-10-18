# Repository guidance

## Before making changes

- Read [docs/architecture.md](docs/architecture.md) for the current system boundaries and flows.
- Check existing tests and follow the patterns in the affected feature.
- Keep architecture documentation aligned with implemented behavior; distinguish existing functionality from proposals.

## Project structure

- `frontend/src`: React and TypeScript single-page application, organized by feature (`auth`, `chat`, `flashcards`) and shared `core`.
- `backend/src`: FastAPI application organized by feature (`auth`, `core`, `flashcards`) with shared database, configuration, filtering, pagination, and sorting utilities.
- `backend/src/alembic`: database migrations and flashcard seed data.
- `backend/tests` and `frontend/src`: backend and frontend tests.

## Validation

- Frontend: run `npm run build`, `npm run lint`, and focused tests with `npm run test:run -- <test-file>` from `frontend/`.
- Backend: use the existing Docker Compose test setup in `backend/docker-compose-tests.yaml`; run focused pytest tests with `docker compose -f backend/docker-compose-tests.yaml run --rm -e ENV=local -e PGPASSWORD=tutor_password backend pytest <test-path>` from the repository root.
- For database/schema changes, review the Alembic migration and test both the affected database behavior and relevant API behavior.

## Architecture boundaries

- The frontend calls the backend through the shared Axios client in `frontend/src/core/apiClient.ts`; preserve the existing API and bearer-token handling patterns.
- Backend routes should use the existing feature routers, services, schemas, and async SQLAlchemy session dependency rather than accessing the database from frontend code.
- Record significant, accepted architectural decisions as numbered ADRs in `docs/decisions/`. Do not use ADRs to present unapproved proposals as implemented decisions.
