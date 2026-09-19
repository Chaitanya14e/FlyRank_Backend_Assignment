from fastapi import FastAPI, Response, status, Body
from database import get_connection, init_db

app = FastAPI()

init_db()

@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": [
            "/tasks"
        ]
    }

@app.get("/health")
def health():
    return {
        "status": "ok"
    }

@app.get("/tasks")
def get_tasks():
    conn = get_connection()
    cursor = conn.execute("""
        SELECT id, title, done
        FROM tasks
    """)
    rows = cursor.fetchall()
    conn.close()
    tasks = []
    for row in rows:
        tasks.append({
            "id": row["id"],
            "title": row["title"],
            "done": bool(row["done"])
        })
    return {
        "data": tasks
    }

@app.get("/tasks/{id}")
def get_task_by_id(id: int, response: Response):
    conn = get_connection()
    cursor = conn.execute(
        """
        SELECT id, title, done
        FROM tasks
        WHERE id = ?
        """,
        (id,)
    )
    row = cursor.fetchone()
    conn.close()
    if row is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "error": "Task not found"
        }
    task = {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"])
    }
    return {
        "data": task
    }

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: dict = Body(...)):
    if "title" not in task or not isinstance(task["title"], str) or task["title"].strip() == "":
        return Response(
            content='{"error":"Title is required"}',
            media_type="application/json",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    title = task["title"].strip()
    conn = get_connection()
    cursor = conn.execute(
        """
        INSERT INTO tasks (title, done)
        VALUES (?, ?)
        """,
        (title, 0)
    )
    conn.commit()
    new_id = cursor.lastrowid
    cursor = conn.execute(
        """
        SELECT id, title, done
        FROM tasks
        WHERE id = ?
        """,
        (new_id,)
    )
    row = cursor.fetchone()
    conn.close()
    new_task = {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"])
    }
    return {
        "data": new_task
    }

@app.put("/tasks/{id}")
def update_task(
    id: int,
    response: Response,
    updated_task: dict = Body(...)
):
    if (
        "title" not in updated_task
        or not isinstance(updated_task["title"], str)
        or updated_task["title"].strip() == ""
    ):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "error": "Title is required"
        }
    conn = get_connection()
    cursor = conn.execute(
        """
        SELECT id
        FROM tasks
        WHERE id = ?
        """,
        (id,)
    )
    row = cursor.fetchone()
    if row is None:
        conn.close()
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "error": f"Task {id} not found"
        }
    title = updated_task["title"].strip()
    if "done" in updated_task:
        done = 1 if updated_task["done"] else 0
        conn.execute(
            """
            UPDATE tasks
            SET title = ?, done = ?
            WHERE id = ?
            """,
            (title, done, id)
        )
    else:
        conn.execute(
            """
            UPDATE tasks
            SET title = ?
            WHERE id = ?
            """,
            (title, id)
        )
    conn.commit()
    cursor = conn.execute(
        """
        SELECT id, title, done
        FROM tasks
        WHERE id = ?
        """,
        (id,)
    )
    row = cursor.fetchone()
    conn.close()
    task = {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"])
    }
    return {
        "data": task
    }

@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int, response: Response):
    conn = get_connection()
    cursor = conn.execute(
        """
        SELECT id
        FROM tasks
        WHERE id = ?
        """,
        (id,)
    )
    row = cursor.fetchone()
    if row is None:
        conn.close()
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "error": f"Task {id} not found"
        }
    conn.execute(
        """
        DELETE FROM tasks
        WHERE id = ?
        """,
        (id,)
    )
    conn.commit()
    conn.close()
    return