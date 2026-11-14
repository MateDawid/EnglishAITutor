# English AI Tutor

## Run whole app in Debug Mode

1. Start Docker containers
```bash
docker compose -f docker-compose.yml -f docker-compose.debug.yml up -d
```
2. Go to `Run And Debug` (Ctrl + Shift + D) section.
3. Start backend with `Run backend in debug mode` configuration.
4. Start frontend with `Run frontend in debug mode` configuration
 
## Managing backend dependencies

```bash
cd ~/Repositories/EnglishAITutor/backend uv sync
```

```bash
uv add --group dev {package_name}
```

## Database migrations

```bash
docker exec -it english-ai-tutor-backend-1 sh -c "alembic revision --autogenerate -m "<migration_name>""
docker exec -it english-ai-tutor-backend-1 sh -c "alembic upgrade head"
```

## Unit tests run

```bash
docker compose -f backend/docker-compose-tests.yaml run --rm backend pytest tests/flashcard_tests
docker compose -f backend/docker-compose-tests.yaml down -v
```

## Remove __pycache__

```bash
sudo find . -type d -name "__pycache__" -exec rm -rf {} +
```