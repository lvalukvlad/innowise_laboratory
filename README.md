# Innowise Python Laboratory

Progressive Python track from Innowise laboratory: from language basics to a containerized REST API.

## Lectures

| Lecture | Focus |
|---------|--------|
| 1–3 | Python fundamentals and small console scripts |
| 4 | SQL: schema, queries, SQLite (`school.db`) |
| 5 | REST Book Collection API (FastAPI / uvicorn) |
| 6 | Docker & Docker Compose: containerized Book API + healthcheck |

## Quick start (lecture 6 — final app)

Requirements: Docker and Docker Compose.

```bash
cd lecture_6
docker compose up --build
```

Healthcheck:

```bash
curl http://localhost:8000/healthcheck
```

Expected response: `{"status": "ok"}`.

Stop:

```bash
docker compose down
```

Alternative without Compose:

```bash
cd lecture_6
docker build . -t app:latest
docker run -p 8000:8000 app:latest
```

More detail: see [`lecture_6/README.md`](lecture_6/README.md).

## Stack

Python · SQL / SQLite · FastAPI · Docker · Docker Compose
