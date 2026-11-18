from app.db import get_connection

with get_connection() as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT version();")
        print(cursor.fetchone())