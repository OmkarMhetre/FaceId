import pymysql
from datetime import datetime
from backend.db.db import get_db_connection


def mark_attendance(name: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    today = datetime.now().date()
    current_time = datetime.now().time()

    try:
        cursor.execute(
            """
            INSERT INTO attendance (name, date, time)
            VALUES (%s, %s, %s)
            """,
            (name, today, current_time)
        )
        conn.commit()

    except pymysql.err.IntegrityError:
        pass

    finally:
        cursor.close()
        conn.close()
