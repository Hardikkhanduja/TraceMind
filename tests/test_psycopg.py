import psycopg

conn = psycopg.connect(
    host="localhost",
    port=5433,
    dbname="tracemind",
    user="postgres",
    password="postgres",
)

print("Connected!")

conn.close()