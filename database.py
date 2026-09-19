import sqlite3

DATABASE = "tasks.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()

    # Create tasks table if it doesn't exist
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    """)

    # Check if table is empty
    cursor = conn.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]

    # Insert seed data only if table is empty
    if count == 0:
        conn.executemany(
            """
            INSERT INTO tasks (title, done)
            VALUES (?, ?)
            """,
            [
                ("Learning FastAPI", 1),
                ("Doing Leetcode problems", 1),
                ("Notes Making", 0)
            ]
        )

    conn.commit()
    conn.close()