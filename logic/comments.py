from datetime import datetime
from db import get_connection, set_row_factory
from logic.tasks import validate_task_access
from errors import *

def row_to_dict(row):
	return {"comment_id": row["comment_id"], "task_id": row["task_id"], "user_id": row["user_id"], "content": row["content"], "created_at": row["created_at"]}


def row_to_list(rows):
	return [row_to_dict(row) for row in rows]
		

def create_comment(user_id, task_id, content):
	conn = get_connection()
	set_row_factory(conn)
	cur = conn.cursor()
	
	task = validate_task_access(cur, task_id, user_id)
	if task in (NOT_FOUND, FORBIDDEN):
		return task
	
	created_at = str(datetime.now())
	
	cur.execute("INSERT INTO comments (task_id, user_id, content, created_at) VALUES (:task_id, :user_id, :content, :created_at)", {"task_id": task_id, "user_id": user_id, "content": content, "created_at": created_at})
	conn.commit()
	
	cur.execute("SELECT comment_id, task_id, user_id, content, created_at FROM comments WHERE comment_id = :id", {"id": cur.lastrowid})
	comment = cur.fetchone()
	conn.close()
	
	return row_to_dict(comment)


def get_comments(user_id, task_id):
	conn = get_connection()
	set_row_factory(conn)
	cur = conn.cursor()
	
	task = validate_task_access(cur, task_id, user_id)
	if task in (NOT_FOUND, FORBIDDEN):
		return task
		
	cur.execute("SELECT comment_id, task_id, user_id, content, created_at FROM comments WHERE task_id = :task_id", {"task_id": task_id})
	comments = cur.fetchall()
	
	conn.close()
	
	return row_to_list(comments)
	
	
def delete_comment(user_id, comment_id):
	conn = get_connection()
	set_row_factory(conn)
	cur = conn.cursor()
	
	cur.execute("SELECT comment_id, task_id, user_id, content, created_at FROM comments WHERE comment_id = :comment_id", {"comment_id": comment_id})
	comment = cur.fetchone()
	
	if comment is None:
		return NOT_FOUND
	if user_id != comment["user_id"]:
		return FORBIDDEN
	
	cur.execute("DELETE FROM comments WHERE comment_id = :comment_id", {"comment_id": comment_id})
	
	conn.commit()
	conn.close()
	
	return row_to_dict(comment)