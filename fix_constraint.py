import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Mihir@197',
    database='quiz_app2'
)
cursor = conn.cursor()

try:
    # Drop the problematic foreign key constraint
    cursor.execute("ALTER TABLE answers1 DROP FOREIGN KEY answers1_ibfk_2")
    
    # Add the correct foreign key constraint
    cursor.execute("ALTER TABLE answers1 ADD CONSTRAINT answers1_ibfk_2 FOREIGN KEY (question_id) REFERENCES questions1(id)")
    
    conn.commit()
    print("Foreign key constraint fixed successfully!")
    
except mysql.connector.Error as err:
    print(f"Error: {err}")
    
finally:
    cursor.close()
    conn.close()