import sqlite3
import os

DATABASE_NAME = os.path.join(os.path.dirname(__file__), "attendance.db")


def connect_database():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    return connection, cursor


def create_tables():

    connection, cursor = connect_database()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        face_registered INTEGER DEFAULT 0
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS course(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_name TEXT,
        instructor TEXT,
        instructor_email TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        feedback TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        student_number TEXT,
        student_name TEXT,
        class_number INTEGER,
        attendance_date TEXT,
        month TEXT,
        status TEXT
    )
    """)

    connection.commit()
    connection.close()


def update_database():

    connection, cursor = connect_database()

    cursor.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in cursor.fetchall()]

    if "face_registered" not in columns:
        cursor.execute("""
        ALTER TABLE users
        ADD COLUMN face_registered INTEGER DEFAULT 0
        """)

    connection.commit()
    connection.close()


def insert_default_course():

    connection, cursor = connect_database()

    cursor.execute("SELECT COUNT(*) FROM course")

    if cursor.fetchone()[0] == 0:

        cursor.execute("""
        INSERT INTO course
        (
            course_name,
            instructor,
            instructor_email
        )
        VALUES
        (
            'Artificial Intelligence',
            'ABC',
            'abc@email.com'
        )
        """)

    connection.commit()
    connection.close()


# ===========================================================
# USER FUNCTIONS
# ===========================================================

def user_exists(username):

    connection, cursor = connect_database()

    cursor.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    )

    user = cursor.fetchone()

    connection.close()

    return user is not None


def register_user(username, password, role):

    connection, cursor = connect_database()

    cursor.execute("""
    INSERT INTO users
    (
        username,
        password,
        role,
        face_registered
    )
    VALUES
    (?, ?, ?, ?)
    """,
    (
        username,
        password,
        role,
        1
    ))

    connection.commit()
    connection.close()

# ===========================================================
# UPDATE PASSWORD
# ===========================================================

def update_password(username, password):

    connection, cursor = connect_database()

    cursor.execute(
        """
        UPDATE users
        SET password=?
        WHERE username=?
        """,
        (
            password,
            username
        )
    )

    connection.commit()

    connection.close()

# ===========================================================
# COURSE
# ===========================================================

def get_course():

    connection, cursor = connect_database()

    cursor.execute(
        "SELECT * FROM course LIMIT 1"
    )

    course = cursor.fetchone()

    connection.close()

    return course


# ===========================================================
# FEEDBACK
# ===========================================================

def save_feedback(username, feedback):

    connection, cursor = connect_database()

    cursor.execute(
        """
        INSERT INTO feedback
        (
            username,
            feedback
        )
        VALUES
        (?,?)
        """,
        (
            username,
            feedback
        )
    )

    connection.commit()
    connection.close()


# ===========================================================
# ATTENDANCE
# ===========================================================

def save_attendance(

    username,
    student_number,
    student_name,
    class_number,
    attendance_date,
    month,
    status

):

    connection, cursor = connect_database()

    cursor.execute(
        """
        INSERT INTO attendance
        (
            username,
            student_number,
            student_name,
            class_number,
            attendance_date,
            month,
            status
        )

        VALUES
        (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            username,
            student_number,
            student_name,
            class_number,
            attendance_date,
            month,
            status
        )
    )

    connection.commit()
    connection.close()


def get_student_attendance(username):

    connection, cursor = connect_database()

    cursor.execute(
        """
        SELECT
            class_number,
            month,
            status

        FROM attendance

        WHERE username=?

        ORDER BY class_number
        """,
        (username,)
    )

    data = cursor.fetchall()

    connection.close()

    return data


def get_all_students():

    connection, cursor = connect_database()

    cursor.execute(
        """
        SELECT username
        FROM users
        WHERE role='Student'
        ORDER BY username
        """
    )

    students = cursor.fetchall()

    connection.close()

    return students

# ===========================================================
# CHECK ATTENDANCE
# ===========================================================

def attendance_exists(username, class_number):

    connection, cursor = connect_database()

    cursor.execute(
        """
        SELECT id
        FROM attendance
        WHERE username=?
        AND class_number=?
        """,
        (
            username,
            class_number
        )
    )

    record = cursor.fetchone()

    connection.close()

    return record is not None

# ===========================================================
# UPDATE ATTENDANCE
# ===========================================================

def update_attendance(

    username,
    class_number,
    status,
    attendance_date,
    month

):

    connection, cursor = connect_database()

    cursor.execute(
        """
        UPDATE attendance

        SET

        status=?,
        attendance_date=?,
        month=?

        WHERE

        username=?
        AND class_number=?
        """,

        (
            status,
            attendance_date,
            month,
            username,
            class_number
        )
    )

    connection.commit()

    connection.close()
# ===========================================================

def initialize_database():

    create_tables()
    update_database()
    insert_default_course()


if __name__ == "__main__":

    initialize_database()

    print("Database Ready")