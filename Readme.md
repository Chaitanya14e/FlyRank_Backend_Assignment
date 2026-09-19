# Task API - PostgreSQL + Docker

A FastAPI Task API connected to PostgreSQL using Docker Compose.

## Why PostgreSQL?

PostgreSQL is used as the persistent database instead of the previous
in-memory/SQLite storage. This allows task data to survive application
and container restarts.

## Architecture

Routes → Service → PostgreSQL Repository → PostgreSQL

The service and API routes remain independent of the database implementation.
The PostgreSQL repository implements the existing TaskRepository interface.

## Environment Variables

Database configuration is stored in `.env`.

The `.env` file is ignored by Git.

Use `.env.example` as a template.

## Running the Application

Make sure Docker Desktop is running.

Start the complete application with:

```bash
docker compose up --build