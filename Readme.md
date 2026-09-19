# Task API - FastAPI + SQLite

A simple CRUD Task API built using FastAPI and SQLite.

## Technologies

- Python
- FastAPI
- SQLite
- Uvicorn

## Features

- Create tasks
- Read all tasks
- Read a task by ID
- Update tasks
- Delete tasks
- SQLite database persistence
- Parameterized SQL queries
- Automatic database and table creation

## Why SQLite?

SQLite was chosen because it is lightweight and requires no separate
database server.

The database is stored in a single file called `tasks.db`.

It also allows task data to survive when the FastAPI server is restarted.

## Database

The database file is:

```text
tasks.db