import psycopg2

def get_connection():
    try:
        conn = psycopg2.connect(
            host="postgres",
            database="mydb",
            user="admin",
            password="admin",
            connect_timeout=5
        )
        return conn
    except Exception as e:
        print("Database connection error:", e)
        raise