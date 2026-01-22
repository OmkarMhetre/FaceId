import pymysql

def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="face_reco"
    )