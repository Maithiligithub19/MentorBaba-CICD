from werkzeug.security import generate_password_hash
import mysql.connector

hashed_password = generate_password_hash('admin123')

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Mihir@197',
    database='quiz_app2'
)
cursor = conn.cursor()

# Insert admin user
cursor.execute("INSERT INTO users1 (email, password, is_admin) VALUES (%s, %s, %s)", 
               ('admin@g.com', hashed_password, True))

conn.commit()
cursor.close()
conn.close()
print("Admin user created successfully!")