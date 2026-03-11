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

# View students
def view_students(conn):
    """Retrieve and display all student records from the database."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()

        if not students:
            print("No student records found.")
        else:
            print("\n--- Student Records ---")
            for student in students:
                print(f"ID: {student[0]} | Name: {student[1]} | Grade: {student[2]} | Email: {student[3]}")
            print("-----------------------\n")
    except sqlite3.Error as e:
        print(f"Database error: {e}")

# Update student
def update_student(conn):
    """Update an existing student record in the database."""
    view_students(conn)

    try:
        student_id = int(input("Enter the ID of the student to update: "))
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return

    name = input("Enter new name (leave blank to keep current): ").strip()
    grade = input("Enter new grade (leave blank to keep current): ").strip()
    email = input("Enter new email (leave blank to keep current): ").strip()

    # Validate email if provided
    if email and "@" not in email:
        print("Invalid email. Must contain '@'.")
        return

    try:
        cursor = conn.cursor()

        if name:
            cursor.execute("UPDATE students SET name = ? WHERE id = ?", (name, student_id))
        if grade:
            cursor.execute("UPDATE students SET grade = ? WHERE id = ?", (grade, student_id))
        if email:
            cursor.execute("UPDATE students SET email = ? WHERE id = ?", (email, student_id))

        conn.commit()
        print(f"Student ID {student_id} updated successfully!")
    except sqlite3.Error as e:
        print(f"Database error: {e}")