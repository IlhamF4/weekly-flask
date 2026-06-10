import config
from db import get_connection, set_row_factory
from errors import FORBIDDEN, NOT_FOUND

def row_to_list(rows):
	return [row_to_dict(row) for row in rows]


def row_to_dict(row):
	return {"id": row["id"], "title": row["title"], "done": bool(row["done"]), "user_id": row["user_id"], "archived": bool(row["archived"])}
	

def row_count(cur, conditions, params):
	query = "SELECT COUNT(id) as total_rows FROM tasks"
	
	if conditions:
		query += " WHERE " + " AND ".join(conditions)
	
	cur.execute(query, params)
	
	return cur.fetchone()["total_rows"]
	

# Check if user_id is equal to user_id of task
def validate_task_access(cur, user_id, task_id):
	cur.execute("SELECT id, user_id FROM tasks WHERE id = :id", {"id": task_id})
	task = cur.fetchone()
	
	if task is None:
		logger.info("task not found")
		return NOT_FOUND
	#guard task["user_id"] to int
	if user_id != task["user_id"]:
		logger.warning("Unathorized action detected")
		return FORBIDDEN
	
	return task


def is_task_archived(cur, task_id):
	cur.execute("SELECT id, archived FROM tasks WHERE id = :id", {"id": task_id})
	task = cur.fetchone()
	
	return bool(task["archived"])


def get_task(cur, task_id):
	cur.execute("SELECT id, title, done, user_id, archived FROM tasks WHERE id = :id", {"id": task_id})
	
	return cur.fetchone()
	

def add_task(user_id, title):
	conn = get_connection(config.DB_NAME)
	set_row_factory(conn)
	cur = conn.cursor()
	
	cur.execute("INSERT INTO tasks (title, user_id) VALUES (:title, :user_id)", {"title": title, "user_id": user_id})
	conn.commit()
	
	task = get_task(cur, cur.lastrowid)
	
	conn.close()
	
	return row_to_dict(task)


def get_tasks(user_id, done=None, search=None, sort=None, page=1, limit=10):
	conn = get_connection(config.DB_NAME)
	set_row_factory(conn)
	cur = conn.cursor()
	
	limit = max(1, min(limit, 100))
	page = max(1, page)
	offset = (page - 1) * limit
	
	query = "SELECT id, title, done, user_id, archived FROM tasks"
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
	
	#filter
	query += " WHERE " + " AND ".join(conditions)
		
	#sorting
	if sort is None:
		query += " ORDER BY id ASC "
	else:
		query += f" ORDER BY id {sort} "
	
	#pagination
	query += " LIMIT :limit OFFSET :offset"
	params["limit"] = limit
	params["offset"] = offset

	cur.execute(query, params)
	tasks = row_to_list(cur.fetchall())
	total_rows = row_count(cur, conditions, params)
	
	conn.close()
	
	return tasks, total_rows
	
	
def update_task(user_id, task_id, title, done):
	conn = get_connection(config.DB_NAME)
	set_row_factory(conn)
	cur = conn.cursor()
	
	task = validate_task_access(cur, user_id, task_id)
	if task in (NOT_FOUND, FORBIDDEN):
		return task
		
	#use build query here
	if title is not None:
		cur.execute("UPDATE tasks SET title = :title WHERE id = :id", {"title": title, "id": task_id})
	if done is not None:
		cur.execute("UPDATE tasks SET done = :done WHERE id = :id", {"done": done, "id": task_id})
	conn.commit()
	
	task = get_task(cur, task_id)
	
	conn.close()
	
	return row_to_dict(task)

	
def delete_task(user_id, task_id):
	conn = get_connection(config.DB_NAME)
	set_row_factory(conn)
	cur = conn.cursor()
	
	task = validate_task_access(cur, user_id, task_id)
	if task in (NOT_FOUND, FORBIDDEN):
		return task
	
	task = get_task(cur, task_id)
		
	cur.execute("DELETE FROM tasks WHERE id = :id", {"id": task_id})
	conn.commit()
	
	conn.close()
	
	return row_to_dict(task)
	
	
def set_archive_task(user_id, task_id, archived):
	conn = get_connection(config.DB_NAME)
	set_row_factory(conn)
	cur = conn.cursor()
	
	task = validate_task_access(cur, user_id, task_id)
	if task in (NOT_FOUND, FORBIDDEN):
		return task
		
	cur.execute("UPDATE tasks SET archived = :archived WHERE id = :id", {"archived": archived, "id": task_id})
	conn.commit()
	
	task = get_task(cur, task_id)
	
	conn.close()
	
	return row_to_dict(task)