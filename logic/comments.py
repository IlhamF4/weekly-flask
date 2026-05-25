import config
from db import get_connection, set_row_factory
from logic.tasks import validate_task_access, is_task_archived
from errors import *

def row_to_dict(row):
	return {"comment_id": row["comment_id"], "task_id": row["task_id"], "user_id": row["user_id"], "content": row["content"], "created_at": row["created_at"]}


def row_to_list(rows):
	return [row_to_dict(row) for row in rows]
	

def validate_comment_access(cur, user_id, comment_id):
	cur.execute("SELECT user_id, deleted FROM comments WHERE comment_id = :comment_id", {"comment_id": comment_id})
	comment = cur.fetchone()
	
	if comment is None: 
		return NOT_FOUND
	if user_id != int(comment["user_id"]):
		return FORBIDDEN
	
	return comment

def get_comment(cur, comment_id):
	cur.execute("SELECT comment_id, task_id, user_id, content, created_at, deleted FROM comments WHERE comment_id = :comment_id", {"comment_id": comment_id})
	return cur.fetchone()
		

def add_comment(user_id, task_id, content):
	conn = get_connection(config.DB_NAME)
	set_row_factory(conn)
	cur = conn.cursor()
	
	task = validate_task_access(cur, user_id, task_id)
	if task in (NOT_FOUND, FORBIDDEN):
		return task
	
	if is_task_archived(cur, task_id):
		return FORBIDDEN
	
	cur.execute("INSERT INTO comments (task_id, user_id, content) VALUES (:task_id, :user_id, :content)", {"task_id": task_id, "user_id": user_id, "content": content})
	conn.commit()
	
	cur.execute("SELECT comment_id, task_id, user_id, content, created_at FROM comments WHERE comment_id = :id", {"id": cur.lastrowid})
	comment = cur.fetchone()
	conn.close()
	
	return row_to_dict(comment)


def get_comments(user_id, task_id, include_deleted=False, page=1, limit=10):
	conn = get_connection(config.DB_NAME)
	set_row_factory(conn)
	cur = conn.cursor()
	
	task = validate_task_access(cur, user_id, task_id)
	if task in (NOT_FOUND, FORBIDDEN):
		return task
	
	limit = max(1, min(limit, 100))
	page = max(1, page)
	offset = (page - 1) * limit
	
	query = "SELECT comment_id, task_id, user_id, content, created_at FROM comments WHERE task_id = :task_id"
	params = {"task_id": task_id}
	
	if not include_deleted:
		query += " AND deleted = :deleted"
		params["deleted"] = False
	
	query += " LIMIT :limit OFFSET :offset"
	params["limit"] = limit
	params["offset"] = offset
		
	cur.execute(query, params )
	comments = cur.fetchall()
	
	conn.close()
	
	return row_to_list(comments)
	
	
def delete_comment(user_id, comment_id):
	conn = get_connection(config.DB_NAME)
	set_row_factory(conn)
	cur = conn.cursor()
	
	#we can merge into 1 helper function
	#cur.execute("SELECT user_id, deleted FROM comments WHERE comment_id = :comment_id", {"comment_id": comment_id})
#	comment = cur.fetchone()
#	
#	if comment is None: 
#		return NOT_FOUND
#	if user_id != int(comment["user_id"]):
#		return FORBIDDEN
	
	comment = validate_comment_access(cur, user_id, comment_id)
	
	if comment in (NOT_FOUND, FORBIDDEN):
		return comment
	
	if bool(comment["deleted"]) is True:
		return NOT_FOUND
	
	#cur.execute("DELETE FROM comments WHERE comment_id = :comment_id", {"comment_id": comment_id})
	cur.execute("UPDATE comments SET deleted = True WHERE comment_id = :comment_id", {"comment_id": comment_id})
	conn.commit()
	
	#cur.execute("SELECT comment_id, task_id, user_id, content, created_at, deleted FROM comments WHERE comment_id = :comment_id", {"comment_id": comment_id})
#	comment = cur.fetchone()
	comment = get_comment(cur, comment_id)
	
	conn.close()
	
	return row_to_dict(comment) | {"deleted": bool(comment["deleted"])}
	
	
def restore_comment(user_id, comment_id):
	conn = get_connection(config.DB_NAME)
	set_row_factory(conn)
	cur = conn.cursor()
	
	#we can merge into 1 helper function
	comment = validate_comment_access(cur, user_id, comment_id)
	
	if comment in (NOT_FOUND, FORBIDDEN):
		return comment
		
	cur.execute("UPDATE comments SET deleted = False WHERE comment_id = :comment_id", {"comment_id": comment_id})
	conn.commit()
	
	comment = get_comment(cur, comment_id)
	
	conn.close()
	
	return row_to_dict(comment) | {"deleted": bool(comment["deleted"])}