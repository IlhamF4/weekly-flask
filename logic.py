import sqlite3

def get_connection():
	return sqlite3.connect("task.db")


def set_row_factory(conn):
	conn.row_factory = sqlite3.Row


def row_to_list(rows):
	return [row_to_dict(row) for row in rows]


def row_to_dict(row):
	return {"id": row["id"], "title": row["title"], "done": bool(row["done"])}
	

def find_task(task_id):
	conn = get_connection()
	set_row_factory(conn)
	cur = conn.cursor()

	cur.execute("SELECT id, title, done FROM tasks WHERE id = :id", {"id": task_id})
	
	task =  cur.fetchone()
	
	conn.close()
	
	if task is None:
		return None
		
	return row_to_dict(task)
	
	
def init_db():
	conn = get_connection()
	cur = conn.cursor()
	
	cur.execute("""
	CREATE TABLE IF NOT EXISTS tasks(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		title TEXT,
		done BOOLEAN
	)
	""")
	
	conn.commit()
	conn.close()


def add_task(title):
	conn = get_connection()
	set_row_factory(conn)
	cur = conn.cursor()
	
	cur.execute("INSERT INTO tasks (title, done) VALUES (:title, :done)", {"title": title, "done": False})
	conn.commit()
	
	cur.execute("SELECT id, title, done FROM tasks WHERE id = :id", {"id": cur.lastrowid})
	task = row_to_dict(cur.fetchone())
	conn.close()
	
	return task


def get_tasks():
	conn = get_connection()
	set_row_factory(conn)
	cur = conn.cursor()
	
	cur.execute("SELECT id, title, done FROM tasks")
	tasks = row_to_list(cur.fetchall())
	conn.close()
	
	return tasks
	
	
def update_task(task_id, title, done):
	conn = get_connection()
	set_row_factory(conn)
	cur = conn.cursor()
	
	task = find_task(task_id)
	
	if task is None:
		return None
		
	if title is not None:
		cur.execute("UPDATE tasks SET title = :title WHERE id = :id", {"title": title, "id": task_id})
	if done is not None:
		cur.execute("UPDATE tasks SET done = :done WHERE id = :id", {"done": done, "id": task_id})
		
	conn.commit()
	conn.close()
	
	return find_task(task_id)

	
def delete_task(task_id):
	conn = get_connection()
	set_row_factory(conn)
	cur = conn.cursor()
	
	task = find_task(task_id)
	
	if task is None:
		return None
		
	cur.execute("DELETE FROM tasks WHERE id = :id", {"id": task_id})
	
	conn.commit()
	conn.close()
	
	return task