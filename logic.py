import sqlite3

def get_connection():
	return sqlite3.connect("task.db")


def set_row_factory(conn):
	conn.row_factory = sqlite3.Row


def tasks_row_list(rows):
	return [tasks_row_dict(row) for row in rows]


def tasks_row_dict(row):
	return {"id": row["id"], "title": row["title"], "done": bool(row["done"])}
	
	
def users_row_list(rows):
	return [users_row_dict(row) for row in rows]


def users_row_dict(row):
	return {"user_id": row["user_id"], "username": row["username"]}


def find_task(task_id):
	conn = get_connection()
	set_row_factory(conn)
	cur = conn.cursor()

	cur.execute("SELECT id, title, done FROM tasks WHERE id = :id", {"id": task_id})
	
	task =  cur.fetchone()
	
	conn.close()
	
	if task is None:
		return None
		
	return tasks_row_dict(task)
	

def check_user(user_id):
	conn = get_connection()
	cur = conn.cursor()
	
	cur.execute("SELECT id FROM users WHERE id = :id", {"id": user_id})
	
	result = cur.fetchone()
	
	conn.close()
	
	return result

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
	
	cur.execute("""
		CREATE TABLE IF NOT EXISTS users(
			user_id INTEGER PRIMARY KEY AUTOINCREMENT,
			username TEXT
		)
	""")
	
	conn.commit()
	conn.close()


# Users area
def add_user(username):
	conn = get_connection()
	set_row_factory(conn)
	cur = conn.cursor()
	
	cur.execute("INSERT INTO users (username) VALUES (:username)", {"username": username})
	conn.commit()
	
	cur.execute("SELECT user_id, username FROM users WHERE user_id = :user_id", {"user_id": cur.lastrowid})
	user = users_row_dict(cur.fetchone())
	
	return user


def get_users():
	conn = get_connection()
	set_row_factory(conn)
	cur = conn.cursor()
	
	cur.execute("SELECT user_id, username FROM users")
	users = users_row_list(cur.fetchall())
	
	conn.close()
	
	return users
	
	
# Tasks area
def add_task(title):
	conn = get_connection()
	set_row_factory(conn)
	cur = conn.cursor()
	
	cur.execute("INSERT INTO tasks (title, done) VALUES (:title, :done)", {"title": title, "done": False})
	conn.commit()
	
	cur.execute("SELECT id, title, done FROM tasks WHERE id = :id", {"id": cur.lastrowid})
	task = tasks_row_dict(cur.fetchone())
	conn.close()
	
	return task


def get_tasks(done=None, search=None, sort=None, page=1, limit=10):
	conn = get_connection()
	set_row_factory(conn)
	cur = conn.cursor()
	
	offset = (page - 1) * limit
	
	query = "SELECT id, title, done FROM tasks "
	params = {}
	conditions = []
	
	if done is not None:
		conditions.append("done = :done")
		params["done"] = int(done)
	#return done
	if search is not None:
		conditions.append("title LIKE :search")
		params["search"] = f"%{search}%"
		
	if conditions:
		query += " WHERE " + " AND ".join(conditions)
		
	if sort is not None:
		#return sort
		query += f" ORDER BY id {sort} "
		#params["sort"] = f"{sort}"
	
	query += " LIMIT :limit OFFSET :offset"
	params["limit"] = limit
	params["offset"] = offset

	cur.execute(query, params)
	tasks = tasks_row_list(cur.fetchall())
	
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