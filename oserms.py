
import mysql.connector

# ----------------------------
# User-defined data type to store DB connection properties
class DBProperties:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

# ----------------------------
# Establishes and returns a connection to the MySQL database.
# ----------------------------
def connect_db(db_props):
    return mysql.connector.connect(
        host=db_props.host,
        user=db_props.user,
        password=db_props.password,
        database=db_props.database
    )


# ----------------------------
# Calculates and returns the grade based on marks obtained.
# ----------------------------
def calculate_grade(marks):
    if marks >= 91:
        return 'A1'
    elif marks >= 81:
        return 'A2'
    elif marks >= 71:
        return 'B1'
    elif marks >= 61:
        return 'B2'
    elif marks >= 51:
        return 'C1'
    elif marks >= 41:
        return 'C2'
    elif marks >= 33:
        return 'D'
    else:
        return 'E'

# ----------------------------
# Adds a student's exam result to the database for the logged-in teacher's subject.
# ----------------------------
def add_student_result(cursor, conn, teacher_id):
    student_id = input("Enter Student ID: ").strip()
    exam_type = input("Enter Exam Type (e.g., Term 1): ").strip()
    marks_obtained = int(input("Enter Marks Obtained (0–100): ").strip())

    # Get subject_id of the logged-in teacher
    cursor.execute("SELECT subject_id FROM teachers WHERE teacher_id = %s", (teacher_id,))
    subject = cursor.fetchone()
    if not subject:
        print("Teacher subject not found.")
        return
    subject_id = subject[0]

    # Validate student existence
    cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
    if not cursor.fetchone():
        print("Student ID does not exist.")
        return

    grade = calculate_grade(marks_obtained)

    # Insert result into the results table
    query = """
    INSERT INTO results (student_id, subject_id, exam_type, marks_obtained, grade)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (student_id, subject_id, exam_type, marks_obtained, grade))
    conn.commit()
    print(" Result added successfully.")

# ----------------------------
# Adds co-scholastic grades and remarks for a student.
# ----------------------------
def add_co_scholastic(cursor, conn):
    student_id = input("Enter Student ID: ").strip()
    term = input("Enter Term (e.g., Term 1): ").strip()
    discipline = input("Enter Discipline Grade (A–E): ").strip().upper()
    work_edu = input("Enter Work Education Grade (A–E): ").strip().upper()
    art_edu = input("Enter Art Education Grade (A–E): ").strip().upper()
    remarks = input("Enter Remarks: ").strip()

    # Insert co-scholastic entry into the co_scholastic table
    query = """
    INSERT INTO co_scholastic (student_id, term, discipline, work_education, art_education, remarks)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (student_id, term, discipline, work_edu, art_edu, remarks))
    conn.commit()
    print("Co-scholastic record added.")

# ----------------------------
# Displays the result card and co-scholastic grades for a given student.
# ----------------------------
def view_student_result(cursor):
    student_id = input("Enter Student ID: ").strip()

    # Get student info
    cursor.execute("SELECT name, class FROM students WHERE student_id = %s", (student_id,))
    student = cursor.fetchone()
    if not student:
        print("Student not found.")
        return
    name, student_class = student
    print(f"\n--- Result Card for {name} (Class {student_class}) ---\n")

    # Get subject-wise marks and grades
    cursor.execute("""
    SELECT s.subject_name, r.exam_type, r.marks_obtained, r.grade
    FROM results r
    JOIN subjects s ON r.subject_id = s.subject_id
    WHERE r.student_id = %s
    ORDER BY r.exam_type, s.subject_name
    """, (student_id,))
    results = cursor.fetchall()

    if results:
        print("Subject             Exam        Marks   Grade")
        print("-" * 45)
        for subject, exam_type, marks, grade in results:
            print(f"{subject:<20} {exam_type:<10} {marks:<7} {grade}")
    else:
        print("No results found.")

    # Display co-scholastic grades
    print("\n--- Co-Scholastic Grades ---")
    cursor.execute("""
    SELECT term, discipline, work_education, art_education, remarks
    FROM co_scholastic
    WHERE student_id = %s
    """, (student_id,))
    coschol = cursor.fetchall()
    if coschol:
        for term, d, w, a, r in coschol:
            print(f"\nTerm: {term}")
            print(f"Discipline: {d}, Work Education: {w}, Art Education: {a}")
            print(f"Remarks: {r}")
    else:
        print("No co-scholastic data found.")

# ----------------------------
# (Duplicate) Displays the result card and co-scholastic grades for a given student.
# ----------------------------
# def view_student_result(cursor):
#     # This function is a duplicate of the previous one and should be removed or renamed.
#     # ...existing code...

# ----------------------------
# Handles teacher login and presents the teacher menu for result and co-scholastic entry.
# ----------------------------s
def teacher_login(cursor, conn):
    username = input("Enter Username: ").strip()
    password = input("Enter Password: ").strip()

    query = "SELECT teacher_id, name FROM teachers WHERE username=%s AND password=%s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    if result:
        global teacher_id, teacher_name
        teacher_id, teacher_name = result
        print(f"\nWelcome, {teacher_name} ({teacher_id})!\n")

        while True:
            print("\n--- Teacher Menu ---")
            print("1. Add Student Result")
            print("2. Add Co-Scholastic Grades")
            print("3. Display Student Result Teacher Wise")
            print("4. Logout")

            choice = input("Enter choice: ").strip()

            if choice == "1":
                add_student_result(cursor, conn, teacher_id)
            elif choice == "2":
                add_co_scholastic(cursor, conn)
            elif choice == "3":
                display_student_details_teacher_wise(cursor, conn, teacher_id);
                
            elif choice == "4":
                print("Logging out...\n")
                break            
                
            else:
                print("Invalid choice. Try again.")
    else:
        print("Invalid username or password.")

# ----------------------------
# Main program loop for user interaction and menu navigation.
# ----------------------------
def main():
    print("Enter database connection details:")
    host = input("Host (default: localhost): ").strip() or "localhost"
    user = input("User (default: root): ").strip() or "root"
    password = input("Password: ").strip()
    database = input("Database name: ").strip()
    db_props = DBProperties(host, user, password, database)

    try:
        conn = connect_db(db_props)
        cursor = conn.cursor()
    except Exception as e:
        print(f"Failed to connect to database: {e}")
        return

    while True:
        print("\n--- Online School Exam Result Management ---")
        print("1. Teacher Login")
        print("2. View Student Result")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            teacher_login(cursor, conn)
        elif choice == "2":
            view_student_result(cursor)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

    cursor.close()
    conn.close()



# ----------------------------
# Calculates and returns grade for marks (alternate grading system).
# ----------------------------
def calculate_grade(marks):
    if marks >= 90:
        return 'A+'
    elif marks >= 80:
        return 'A'
    elif marks >= 70:
        return 'B+'
    elif marks >= 60:
        return 'B'
    elif marks >= 50:
        return 'C'
    else:
        return 'F'


# ----------------------------
# Calculates and returns grade for marks (alternate grading system).
# ----------------------------
def display_student_details_teacher_wise(cursor, conn, teacher_id):
    query="""SELECT st.name, st.class, s.subject_name, r.exam_type, r.marks_obtained, r.max_marks,r.grade
FROM results r
JOIN subjects s ON r.subject_id = s.subject_id
JOIN teachers t ON s.subject_id = t.subject_id
join students st on r.student_id = st.student_id
WHERE t.teacher_id = %s and st.class = %s; """
    class_value = input("Enter Class: ").strip()
    cursor.execute(query, (teacher_id,class_value));
    results = cursor.fetchall()
    if results:
        print(f"\n--- Student Details for Teacher ID {teacher_id} ---\n")
        print("Name               Class  Subject         Exam        Marks   Max Marks  Grade")
        print("-" * 75)
        for name, student_class, subject, exam_type, marks, max_marks, grade in results:
            print(f"{name:<18} {student_class:<6} {subject:<15} {exam_type:<10} {marks:<7} {max_marks:<10} {grade}")
    else:
        print("No student details found for this teacher.")

# ----------------------------
# Entry point for running the batch insert program.
# ----------------------------
if __name__ == "__main__":
    main()