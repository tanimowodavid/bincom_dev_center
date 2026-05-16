
# ===========================================================
# Question 1:
# ===========================================================
def fibonacci(n):
    series = []
    a, b = 0, 1

    for _ in range(n):
        series.append(a)
        a, b = b, a + b

    return series

print(fibonacci(10))


# =============================================================
# Question 2, 3 & 4:
# =============================================================

import psycopg2
from psycopg2.extras import execute_values

# =========================
# DATABASE CONNECTION
# =========================
conn = psycopg2.connect(
    dbname="todo_app",
    user="postgres",
    password="your_password",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()

# =========================
# CREATE TABLES
# =========================
def create_tables():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS todos (
        id SERIAL PRIMARY KEY,
        task TEXT NOT NULL,
        completed BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name TEXT,
        age INT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS baby_names (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        rank INT
    );
    """)

    conn.commit()

# =========================
# TODO_CRUD_OPERATIONS
# =========================
def add_task(task):
    cursor.execute("INSERT INTO todos (task) VALUES (%s)", (task,))
    conn.commit()

def get_tasks():
    cursor.execute("SELECT * FROM todos")
    return cursor.fetchall()

def mark_complete(task_id):
    cursor.execute(
        "UPDATE todos SET completed = TRUE WHERE id = %s",
        (task_id,)
    )
    conn.commit()

def delete_task(task_id):
    cursor.execute("DELETE FROM todos WHERE id = %s", (task_id,))
    conn.commit()

# =========================
# USERS CRUD OPERATIONS
# =========================
def add_user(name, age):
    cursor.execute(
        "INSERT INTO users (name, age) VALUES (%s, %s)",
        (name, age)
    )
    conn.commit()

def get_users():
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

def update_user_age(user_id, new_age):
    cursor.execute(
        "UPDATE users SET age = %s WHERE id = %s",
        (new_age, user_id)
    )
    conn.commit()

def delete_user(user_id):
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()

# =========================
# BABY NAMES INSERT
# =========================
import re
with open("2nd_contact_session/baby2008.html", "r") as f:
    content = f.read()

pattern = r'<td>(\d+)</td><td>(\w+)</td><td>(\w+)</td>'
matches = re.findall(pattern, content)

names = [] # list of baby names and their index
for rank, boy, girl in matches:
    names.append((boy, int(rank)))
    names.append((girl, int(rank)))

def insert_baby_names(names):
    """
    names should look like:
    [("Michael", 1), ("Jessica", 1), ...]
    """
    query = "INSERT INTO baby_names (name, rank) VALUES %s"
    execute_values(cursor, query, names)
    conn.commit()

def get_baby_names():
    cursor.execute("SELECT * FROM baby_names ORDER BY rank ASC")
    return cursor.fetchall()

# =========================
# MAIN TEST FLOW
# =========================
if __name__ == "__main__":
    create_tables()

    # --- TODO_TEST ---
    add_task("Learn Python")
    add_task("Finish assignment")

    print("Todos:", get_tasks())

    mark_complete(1)
    delete_task(2)

    print("Todos after update:", get_tasks())

    # --- USERS TEST ---
    add_user("David", 25)
    add_user("Alice", 30)

    print("Users:", get_users())

    update_user_age(1, 26)
    delete_user(2)

    print("Users after update:", get_users())

    # --- BABY NAMES TEST ---
    sample_names = [
        ("Michael", 1),
        ("Jessica", 1),
        ("Christopher", 2),
        ("Ashley", 2)
    ]

    insert_baby_names(sample_names)

    print("Baby Names:", get_baby_names())

    # Close connection
    cursor.close()
    conn.close()

