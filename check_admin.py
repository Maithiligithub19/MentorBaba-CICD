import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Mihir@197',
    database='quiz_app2'
)
cursor = conn.cursor(dictionary=True)
cursor.execute("SELECT * FROM users1 WHERE email = 'admin@g.com'")
user = cursor.fetchone()
print(f"Admin user: {user}")

cursor.execute("SELECT * FROM users1")
all_users = cursor.fetchall()
print(f"All users: {all_users}")

cursor.close()
conn.close()