import mysql.connector
from fastapi import HTTPException
from .hashing import verify_password

MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "face_reco"
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        return conn, cursor
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"MySQL connection error: {str(e)}"
        )


def authenticate_admin(username: str, password: str):
    conn, cursor = get_db_connection()

    try:
        query = """
            SELECT username, password_hash, role
            FROM users
            WHERE username = %s
        """
        cursor.execute(query, (username,))
        row = cursor.fetchone()

        if not row:
            raise HTTPException(status_code=401, detail="Invalid username or password")

        db_username, db_password_hash, role = row

        if role != "ADMIN":
            raise HTTPException(status_code=403, detail="Not authorized")


        if not verify_password(password, db_password_hash):
            raise HTTPException(status_code=401, detail="Invalid username or password")

        return {
            "username": db_username,
            "role": role,
            "message": "Login successful"
        }

    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"MySQL Error: {str(e)}"
        )

    finally:
        cursor.close()
        conn.close()
