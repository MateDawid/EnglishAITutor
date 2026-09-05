# English AI Tutor

## Dev dependency add

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