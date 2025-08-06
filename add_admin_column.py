import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Mihir@197',
    database='quiz_app2'
)
cursor = conn.cursor()

# Add is_admin column
cursor.execute("ALTER TABLE users1 ADD COLUMN is_admin BOOLEAN DEFAULT FALSE")
conn.commit()

cursor.close()
conn.close()
print("is_admin column added successfully!")