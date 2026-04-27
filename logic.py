import sqlite3

FORBIDDEN = "FORBIDDEN"
NOT_FOUND = "NOT_FOUND"

def get_connection():
	return sqlite3.connect("task.db")


def set_row_factory(conn):
	conn.row_factory = sqlite3.Row


def tasks_row_list(rows):
	return [tasks_row_dict(row) for row in rows]


def tasks_row_dict(row):
	return {"id": row["id"], "title": row["title"], "done": bool(row["done"]), "user_id": row["user_id"]}
	
	
def users_row_list(rows):
	return [users_row_dict(row) for row in rows]


def users_row_dict(row):
	return {"user_id": row["user_id"], "username": row["username"]}


def find_task(task_id):
	conn = get_connection()
	set_row_factory(conn)
	cur = conn.cursor()

	cur.execute("SELECT id, title, done, user_id FROM tasks WHERE id = :id", {"id": task_id})
	
	task =  cur.fetchone()
	
	conn.close()
	
	if task is None:
		return NOT_FOUND
		
	return tasks_row_dict(task)
	

def find_user(user_id):
	conn = get_connection()
	set_row_factory(conn)
	cur = conn.cursor()
	
	cur.execute("SELECT user_id, username FROM users WHERE user_id = :user_id", {"user_id": user_id})
	
	result = cur.fetchone()
	
	conn.close()
	
	if result is None:
		return NOT_FOUND
	
	return users_row_dict(result)

def init_db():
	conn = get_connection()
	cur = conn.cursor()
	
	cur.execute("""
	CREATE TABLE IF NOT EXISTS tasks(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		title TEXT,
		done BOOLEAN,
		user_id INTEGER
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


def update_user(user_id, username):
	conn = get_connection()
	set_row_factory(conn)
	cur = conn.cursor()
	
	user = find_user(user_id)
	
	if user == NOT_FOUND:
		return NOT_FOUND
	
	cur.execute("UPDATE users SET username = :username WHERE user_id = :user_id", {"username": username, "user_id": user_id})
	conn.commit()
	
	cur.execute("SELECT user_id, username FROM users WHERE user_id = :user_id", {"user_id": user_id})
	
	user = cur.fetchone()
	
	conn.close()
	
	return users_row_dict(user)

def delete_user(user_id):
	conn = get_connection()
	set_row_factory(conn)
	cur = conn.cursor()
	
	user = find_user(user_id)
	
	if user == NOT_FOUND:
		return NOT_FOUND
	
	cur.execute("DELETE FROM users WHERE user_id = :user_id", {"user_id": user_id})
	
	conn.commit()
	conn.close()
	
	return user
	
# Tasks area
def add_task(user_id, title):
	conn = get_connection()
	set_row_factory(conn)
	cur = conn.cursor()
	
	cur.execute("INSERT INTO tasks (title, done, user_id) VALUES (:title, :done, :user_id)", {"title": title, "done": False, "user_id": user_id})
	conn.commit()
	
	cur.execute("SELECT id, title, done, user_id FROM tasks WHERE id = :id", {"id": cur.lastrowid})
	task = cur.fetchone()
	conn.close()
	
	return tasks_row_dict(task)


def get_tasks(user_id, done=None, search=None, sort=None, page=1, limit=10):
	conn = get_connection()
	set_row_factory(conn)
	cur = conn.cursor()
	
	offset = (page - 1) * limit
	
	query = "SELECT id, title, done, user_id FROM tasks "
	params = {}
	conditions = []
	
	if user_id is not None:
		conditions.append("user_id = :user_id")
		params["user_id"] = user_id
	if done is not None:
		conditions.append("done = :done")
		params["done"] = int(done)
	if search is not None:
		conditions.append("title LIKE :search")
		params["search"] = f"%{search}%"
	
	if conditions:
		query += " WHERE " + " AND ".join(conditions)
		
	if sort is not None:
		query += f" ORDER BY id {sort} "
	
	query += " LIMIT :limit OFFSET :offset"
	params["limit"] = limit
	params["offset"] = offset

	cur.execute(query, params)
	tasks = tasks_row_list(cur.fetchall())
	
	conn.close()
	
	return tasks
	
	
def update_task(user_id, task_id, title, done):
	conn = get_connection()
	set_row_factory(conn)
	cur = conn.cursor()
	
	task = find_task(task_id)
	
	if task == NOT_FOUND:
		return NOT_FOUND
	
	if user_id != task["user_id"]:
		return FORBIDDEN
		
	if title is not None:
		cur.execute("UPDATE tasks SET title = :title WHERE id = :id", {"title": title, "id": task_id})
	if done is not None:
		cur.execute("UPDATE tasks SET done = :done WHERE id = :id", {"done": done, "id": task_id})
	conn.commit()
	
	cur.execute("SELECT id, title, done, user_id FROM tasks WHERE id = :id", {"id": task_id})
	
	task = cur.fetchone()
	
	conn.close()
	
	return tasks_row_dict(task)

	
def delete_task(user_id, task_id):
	conn = get_connection()
	set_row_factory(conn)
	cur = conn.cursor()
	
	task = find_task(task_id)
	
	if task == NOT_FOUND:
		return NOT_FOUND
		
	if user_id != task["user_id"]:
		return FORBIDDEN
		
	cur.execute("DELETE FROM tasks WHERE id = :id", {"id": task_id})
	
	conn.commit()
	conn.close()
	
	return tasks_row_dict(task)