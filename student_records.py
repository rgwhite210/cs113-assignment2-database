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

# Delete student
def delete_student(conn):
    """Delete a student record from the database."""
    view_students(conn)

    try:
        student_id = int(input("Enter the ID of the student to delete: "))
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return

    confirm = input(f"Are you sure you want to delete student ID {student_id}? (yes/no): ").strip().lower()

    if confirm != "yes":
        print("Deletion cancelled.")
        return

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        conn.commit()

        if cursor.rowcount == 0:
            print(f"No student found with ID {student_id}.")
        else:
            print(f"Student ID {student_id} deleted successfully!")
    except sqlite3.Error as e:
        print(f"Database error: {e}")

# Main Menu
def main_menu():
    """Display the main menu and handle user navigation."""
    conn = connect_db()

    while True:
        print("\n---- Student Record Manager ----")
        print("1. Add a new student record")
        print("2. View all student records")
        print("3. Update a student record")
        print("4. Delete a student record")
        print("5. Exit")
        print("==================================\n")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_student(conn)
        elif choice == "2":
            view_students(conn)
        elif choice == "3":
            update_student(conn)
        elif choice == "4":
            delete_student(conn)
        elif choice == "5":
            print("Goodbye!")
            conn.close()
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

# Run Program
if __name__ == "__main__":
    main_menu()