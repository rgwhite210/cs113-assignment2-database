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

# Add student to database
def add_student(conn):
    """Add a new student record to the database."""
    name = input("Enter student name: ").strip()
    grade = input("Enter student grade: ").strip()
    email = input("Enter student email: ").strip()

    # Validate email contains '@'
    if "@" not in email:
        print("Invalid email. Must contain '@'.")
        return

    # Validate name and grade are not empty
    if not name or not grade:
        print("Name and grade cannot be empty.")
        return

    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO students (name, grade, email) VALUES (?, ?, ?)",
            (name, grade, email)
        )
        conn.commit()
        print(f"Student '{name}' added successfully!")
    except sqlite3.Error as e:
        print(f"Database error: {e}")