import psycopg2

# Function to get database connection
def get_db_connection():
    conn = psycopg2.connect(
        host='dpg-ctfciq5ds78s73dopt60-a.oregon-postgres.render.com',  # Replace with environment variables if needed
        database='todo_db_r2wo',
        user='todo_db_r2wo_user',
        password='uNJKvtlXJmqIc43NzYmSwG9zlKTgC5Ks'
    )
    return conn

# Function to fetch all tasks
def get_all_tasks():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM tasks ORDER BY id DESC')
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return tasks

# Function to add a new task
def add_task(task):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO tasks (task) VALUES (%s)', (task,))
    conn.commit()
    cur.close()
    conn.close()

# Function to update a task
def update_task(task_id, new_task):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE tasks SET task = %s WHERE id = %s', (new_task, task_id))
    conn.commit()
    cur.close()
    conn.close()

# Function to delete a task
def delete_task(task_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM tasks WHERE id = %s', (task_id,))
    conn.commit()
    cur.close()
    conn.close()
    
# In models.py
def get_task_by_id(task_id):
    conn = get_db_connection()  # Your function to get a DB connection
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    task = cur.fetchone()  # Fetch the task based on task_id
    cur.close()
    return task  # Returns None if task not found


# Function to delete all tasks
def delete_all_tasks():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM tasks')
    conn.commit()
    cur.close()
    conn.close()
