import data
import sqlite3

def init_db():
	conn = sqlite3.connect("tasks.db")
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


def insert_task(title):
	conn = sqlite3.connect("tasks.db")
	cur = conn.cursor()
	
	cur.execute("INSERT INTO tasks VALUES (?, ?)", (title, False))
	conn.commit()
	conn.close()
	
	task = {"id": cur.lastrowid, "title": title, "done": False}
	
	return task


def get_tasks():
	conn = sqlite3.connect("tasks.db")
	cur = conn.cursor()
	
	cur.execute("SELECT * FROM tasks")
	tasks = cur.fetchall()
	conn.close()
	
	return tasks


def get_tasks():
	return list(data.tasks.values())


def add_task(title):
	new_task = {"id": data.current_id, "title": title, "done": False}
	data.tasks[data.current_id] = new_task
	data.current_id += 1
	return new_task


def update_task(task_id, title, done):
	task = data.tasks.get(task_id)
	
	if task is None:
		return None
	
	if title is not None:
		task["title"] = title
	if done is not None:
		task["done"] = done
		
	return task
	
def delete_task(task_id):
	task = data.tasks.get(task_id)
	
	if task is None:
		return None
		
	del data.tasks[task_id]
	
	return task
	