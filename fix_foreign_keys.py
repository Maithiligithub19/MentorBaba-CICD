import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Mihir@197',
    database='quiz_app2'
)
cursor = conn.cursor()

# Drop existing foreign key constraints
cursor.execute("ALTER TABLE answers1 DROP FOREIGN KEY answers1_ibfk_1")
cursor.execute("ALTER TABLE answers1 DROP FOREIGN KEY answers1_ibfk_2")

# Add correct foreign key constraints
cursor.execute("ALTER TABLE answers1 ADD FOREIGN KEY (user_id) REFERENCES users1(id)")
cursor.execute("ALTER TABLE answers1 ADD FOREIGN KEY (question_id) REFERENCES questions1(id)")

conn.commit()
cursor.close()
conn.close()
print("Foreign keys fixed!")