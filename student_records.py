import sqlite3

# Database Setup
def connect_db():
    """Connect to SQLite database and create table if it doesn't exist."""
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS students ("
        "id INTEGER PRIMARY KEY, "
        "name TEXT NOT NULL, "
        "grade TEXT NOT NULL, "
        "email TEXT NOT NULL)"
    )
    conn.commit()
    return conn

