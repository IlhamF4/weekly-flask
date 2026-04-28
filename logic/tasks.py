from db import get_connection, set_row_factory
from errors import FORBIDDEN, NOT_FOUND


def tasks_row_list(rows):
	return [tasks_row_dict(row) for row in rows]


def tasks_row_dict(row):
	return {"id": row["id"], "title": row["title"], "done": bool(row["done"]), "user_id": row["user_id"]}
	
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
	
	limit = max(1, min(limit, 100))
	page = max(1, page)
	offset = (page - 1) * limit
	
	query = "SELECT id, title, done, user_id FROM tasks "
	params = {}
	conditions = []
	
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
		
	if sort is None:
		query += " ORDER BY id ASC "
	else:
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
	
	cur.execute("SELECT id, title, done, user_id FROM tasks WHERE id = :id", {"id": task_id})
	task = cur.fetchone()
	
	if task is None:
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
	
	cur.execute("SELECT id, title, done, user_id FROM tasks WHERE id = :id", {"id": task_id})
	task = cur.fetchone()
	
	if task is None:
		return NOT_FOUND
		
	if user_id != task["user_id"]:
		return FORBIDDEN
		
	cur.execute("DELETE FROM tasks WHERE id = :id", {"id": task_id})
	
	conn.commit()
	conn.close()
	
	return tasks_row_dict(task)
