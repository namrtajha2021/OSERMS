import mysql.connector
class DBProperties:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
#  DATABASE SETUP AND TABLES
def setup_database(db_props):

    conn = mysql.connector.connect(
        host=db_props.host,
        user=db_props.user,
        password=db_props.password

    )
    cursor = conn.cursor()
    

    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_props.database}`")
    cursor.execute(f"USE `{db_props.database}`")

    # tables

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS subjects (
            subject_id INT AUTO_INCREMENT PRIMARY KEY,
            subject_name VARCHAR(50) NOT NULL
        )
        """
    )


    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS teachers (
            teacher_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50),
            username VARCHAR(50) UNIQUE,
            pwd VARCHAR(255),
            subject_id INT
        )
        """
    )


    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS students (
            student_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50),
            class VARCHAR(10)
        )
        """
    )
        

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS results (
            result_id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            subject_id INT,
            exam_type VARCHAR(20),
            marks_obtained INT,
            grade VARCHAR(2),
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
        )
        """
    )


    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS co_scholastic (
            coschol_id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            term VARCHAR(20),
            discipline CHAR(1),
            work_education CHAR(1),
            art_education CHAR(1),
            remarks VARCHAR(100),
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        )
        """
    )
    

    cursor.execute("SELECT COUNT(*) FROM subjects")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO subjects (subject_name) VALUES (%s)",
            [
                ('Math',),
                ('Physics',),
                ('Chemistry',),
                ('Computer Science',)
            ]
        )

    cursor.execute("SELECT COUNT(*) FROM teachers")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO teachers (name, username, pwd, subject_id) VALUES (%s, %s, %s, %s)",
            [
                ('dilip singh', 'ds', '111', 1),
                ('Rajinder kaur', 'rk', '112', 2),
                ('chaitanya', 'cp', '113', 3),
                ('manoj kumar', 'pt', '114', 4)
            ]
        )


    cursor.execute("SELECT COUNT(*) FROM students")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO students (name, class) VALUES (%s, %s)",
            [
                ('paras garg', '12'),
                ('manish', '12'),
                ('sanyam', '12'),
                ('namrta jha', '12'),
                ('shristi', '12'),
                ('sunny singh', '12'),
                ('sujal', '12'),
                ('vaibhav', '12'),
                ('vedansh', '12'),
                ('jiya', '12'),
                ('rishab', '12'),
                ('anshika', '12'),
                ('jai pawan verma', '12'),
                ('saurabh', '12'),
                ('deepu', '12'),
                ('shubham', '12'),
                ('punit', '12'),
                ('yash bharadwaj', '12'),
                ('hansi', '12'),
                ('himanshi', '12'),
                ('shikha', '12'),
                ('nilakshi', '12')
            ]
        )

    conn.commit()
    cursor.close()
    conn.close()
    
#------------------------------------------------------------------

    print("   ------WELCOME   (^.^)  -------")

#  CONNECT TO DATABASE

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

#  GRADE CALCULATION

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
#  DISPLAY STUDENTS LIST
def show_students(cursor):
    cursor.execute("SELECT student_id, name, class FROM students")
    students = cursor.fetchall()

    if not students:
        print("No students found in database!")
        return []

    print("\nAvailable Students:")
    print("-" * 40)
    print(f"{'ID':<10} {'Name':<20} {'Class':<10}")
    print("-" * 40)
    for s in students:
        print(f"{s[0]:<10} {s[1]:<20} {s[2]:<10}")
    print("-" * 40)

    return [str(s[0]) for s in students]
#  ADD STUDENT RESULT
def add_student_result(cursor, conn, teacher_id):
    available_ids = show_students(cursor)
    if not available_ids:
        return

    student_id = input("Enter Student ID to update: ").strip()
    if student_id not in available_ids:
        print("Invalid Student ID.")
        return

    exam_type = input("Enter Exam Type (e.g., Term 1): ").strip()
    marks_obtained = int(input("Enter Marks Obtained (0–100): ").strip())

    cursor.execute("SELECT subject_id FROM teachers WHERE teacher_id = %s", (teacher_id,))
    subject_id = cursor.fetchone()[0]

    grade = calculate_grade(marks_obtained)

    cursor.execute("""
        INSERT INTO results (student_id, subject_id, exam_type, marks_obtained, grade)
        VALUES (%s, %s, %s, %s, %s)
    """, (student_id, subject_id, exam_type, marks_obtained, grade))

    conn.commit()
    print("Result added successfully!")
#  ADD CO-SCHOLASTIC GRADES
def add_co_scholastic(cursor, conn):
    available_ids = show_students(cursor)
    if not available_ids:
        return

    student_id = input("Enter Student ID to update: ").strip()
    if student_id not in available_ids:
        print("Invalid Student ID.")
        return

    term = input("Enter Term (e.g., Term 1): ").strip()
    discipline = input("Enter Discipline Grade (A–E): ").strip().upper()
    work_edu = input("Enter Work Education Grade (A–E): ").strip().upper()
    art_edu = input("Enter Art Education Grade (A–E): ").strip().upper()
    remarks = input("Enter Remarks: ").strip()

    cursor.execute("""
        INSERT INTO co_scholastic (student_id, term, discipline, work_education, art_education, remarks)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (student_id, term, discipline, work_edu, art_edu, remarks))
    conn.commit()
    print(" Co-scholastic record added successfully!")

#  VIEW STUDENT RESULT
def view_student_result(cursor):
    student_id = input("Enter Student ID: ").strip()

    cursor.execute("SELECT name, class FROM students WHERE student_id = %s", (student_id,))
    student = cursor.fetchone()
    if not student:
        print("Student not found.")
        return

    name, student_class = student
    print(f"\n--- Result Card for {name} (Class {student_class}) ---\n")

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

    print("\n--- Co-Scholastic Grades ---")
    cursor.execute("""
        SELECT term, discipline, work_education, art_education, remarks
        FROM co_scholastic WHERE student_id = %s
    """, (student_id,))
    coschol = cursor.fetchall()

    if coschol:
        for term, d, w, a, r in coschol:
            print(f"\nTerm: {term}")
            print(f"Discipline: {d}, Work Education: {w}, Art Education: {a}")
            print(f"Remarks: {r}")
    else:
        print("No co-scholastic data found.")

#  DISPLAY STUDENT DETAILS TEACHER-WISE

def display_student_details_teacher_wise(cursor, conn, teacher_id):
    class_value = input("Enter Class: ").strip()

    query = """
    SELECT st.name, st.class, s.subject_name, r.exam_type, r.marks_obtained, r.grade, 
    co_scholastic.discipline,co_scholastic.work_education,co_scholastic.art_education,co_scholastic.remarks  
        FROM results r
        JOIN subjects s ON r.subject_id = s.subject_id
        JOIN teachers t ON s.subject_id = t.subject_id
        JOIN students st ON r.student_id = st.student_id
        join co_scholastic on r.student_id = co_scholastic.student_id 
        WHERE t.teacher_id = %s AND st.class = %s
    """
    cursor.execute(query, (teacher_id, class_value))
    results = cursor.fetchall()

    if results:
        print(f"\n--- Student Details for Class {class_value} ---\n")
        print("Name               Class  Subject         Exam        Marks   Grade  Discipline WorkEdu ArtEdu Remarks")
        print("-" * 100)
        for name, student_class, subject, exam_type, marks, grade, discipline, work_education, art_education, remarks in results:
            print(f"{name:<18} {student_class:<6} {subject:<15} {exam_type:<10} {marks:<7} {grade:<7} {discipline:<7}     {work_education}      {art_education}    {remarks}")
    else:
        print("No student details found for this teacher.")




#  TEACHER LOGIN & MENU

def teacher_login(cursor, conn):
    print("\n===== TEACHER LOGIN =====")
    
    cursor.execute("""
        SELECT t.teacher_id, t.name, t.username, s.subject_name
        FROM teachers t
        JOIN subjects s ON t.subject_id = s.subject_id
    """)
    teachers = cursor.fetchall()

    if not teachers:
        print("No teachers found in database!")
        return None

    print("\nAvailable Teachers:")
    print("-" * 70)
    print(f"{'ID':<5} {'Name':<20} {'Username':<20} {'Subject':<20}")
    print("-" * 70)
    for t in teachers:
        print(f"{t[0]:<5} {t[1]:<20} {t[2]:<20} {t[3]:<20}")
    print("-" * 70)

    try:
        selected_id = int(input("\nEnter your Teacher ID to login: ").strip())
    except ValueError:
        print("Invalid input. Please enter a numeric ID.")
        return None

    cursor.execute("""
        SELECT t.teacher_id, t.name, s.subject_name
        FROM teachers t
        JOIN subjects s ON t.subject_id = s.subject_id
        WHERE t.teacher_id=%s
    """, (selected_id,))
    result = cursor.fetchone()

    if result:
        teacher_id, teacher_name, teacher_subject = result
        print(f"\n Login successful! Welcome, {teacher_name} ({teacher_subject}).\n")

        while True:
            print(f"\n--- Teacher Menu ({teacher_name} - {teacher_subject}) ---")
            print("1. Add Student Result")
            print("2. Add Co-Scholastic Grades")
            print("3. Display Student Details (Teacher-wise)")
            print("4. Logout")

            choice = input("Enter choice: ").strip()
            if choice == "1":
                add_student_result(cursor, conn, teacher_id)
            elif choice == "2":
                add_co_scholastic(cursor, conn)
            elif choice == "3":
                display_student_details_teacher_wise(cursor, conn, teacher_id)
            elif choice == "4":
                print("Logging out...\n")
                break
            else:
                print("Invalid choice. Try again.")
    else:
        print("Invalid Teacher ID. Try again.")

#  MAIN PROGRAM LOOP

def main(db_props):
    conn = connect_db(db_props)
    cursor = conn.cursor()

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

#  ENTRY POINT
if __name__ == "__main__":
    print("Enter database connection details:")
    host = input("Host (default: localhost): ").strip() or "localhost"
    user = input("User (default: root): ").strip() or "root"
    password = input("Password: ").strip()
    database = input("Database name: ").strip()
    db_props = DBProperties(host, user, password, database)
    setup_database(db_props)
    main(db_props)
