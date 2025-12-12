# YABA - Yet Another Budgeting App

A self hostable APIi for personal expense tracking built with FastAPI

## Context

There are many great opensource options for personal finance tracking. However, I felt like they were either too feature full or lacking particular features I was looking for.
YABA strives to achieve a middle ground where it can track your personal finances and share the progress with your significant other so that multiple people can register expenses on the same account.

WARNING: This API is still in early stages of development.

## Technology

I chose FastAPI because python was my first language and since I'm not a backend engineer, I prefered to ignore the barrier of a new language to make it easier to progress.
I've built a couple tools using Django and worked in a professional setting with Flask, so I wanted to learn a new framework and FastAPI seemed promissing.



## Setup

1. Copy `.env.example` to `.env` and fill in secrets.
2. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

3. Run the app:

   ```sh
   uvicorn app.main:app --reload
   ```

## API Endpoints

- `/api/auth/register` — Register user
- `/api/auth/login` — Login user (returns JWT)
- `/api/users/me` — Get current user
- `/api/users/` — CRUD users

## Docker

Build and run with Docker:

```sh
docker build -t budget-app .
docker run -p 8000:8000 --env-file .env budget-app
```

## Running Tests

To run the backend test suite:

```sh
PYTHONPATH=. pytest
```

This will execute all tests in the `tests/` directory using your current environment and database. For a clean test run, ensure your virtual environment is activated and dependencies are installed.

## API Documentation

When the backend server is running, interactive API documentation is automatically generated and available via Swagger UI. To access it, open your browser and navigate to:

- `http://localhost:8000/docs` for Swagger UI
- `http://localhost:8000/openapi.json` for the raw OpenAPI specification

These endpoints allow you to explore and test your API interactively.

## License

MIT
