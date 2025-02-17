import sqlite3
import random
from faker import Faker

# Initialize Faker for generating fake data
fake = Faker()

# Connect to SQLite
db_name = "student_info.db"
connection = sqlite3.connect(db_name)
cursor = connection.cursor()

# Create the STUDENT_INFO table
table_info = """
CREATE TABLE STUDENT_INFO (
    ID INTEGER PRIMARY KEY,
    NAME VARCHAR(50),
    AGE INT,
    GENDER VARCHAR(10),
    CLASS VARCHAR(20),
    SECTION VARCHAR(5),
    MARKS INT,
    EMAIL VARCHAR(50),
    PHONE VARCHAR(15),
    ADDRESS TEXT
);
"""
cursor.execute(table_info)

# Generate and insert 1000 student records
classes = ["Data Science", "Machine Learning", "Cybersecurity", "DevOps", "Software Engineering"]
sections = ["A", "B", "C", "D"]
genders = ["Male", "Female", "Other"]

students = []
for i in range(1000):
    name = fake.name()
    age = random.randint(18, 30)
    gender = random.choice(genders)
    student_class = random.choice(classes)
    section = random.choice(sections)
    marks = random.randint(30, 100)
    email = fake.email()
    phone = fake.phone_number()
    address = fake.address().replace("\n", " ")
    students.append((name, age, gender, student_class, section, marks, email, phone, address))

cursor.executemany("""INSERT INTO STUDENT_INFO (NAME, AGE, GENDER, CLASS, SECTION, MARKS, EMAIL, PHONE, ADDRESS) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", students)

# Commit and close
connection.commit()
connection.close()

print(f"Database '{db_name}' with 1000 student records created successfully!")