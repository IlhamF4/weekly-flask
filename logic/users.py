from db import get_connection, set_row_factory
from errors import FORBIDDEN, NOT_FOUND

def users_row_list(rows):
	return [users_row_dict(row) for row in rows]


def users_row_dict(row):
	return {"user_id": row["user_id"], "username": row["username"]}

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


def add_user(username):
	conn = get_connection()
	set_row_factory(conn)
	cur = conn.cursor()
	
	cur.execute("INSERT INTO users (username) VALUES (:username)", {"username": username})
	conn.commit()
	
	cur.execute("SELECT user_id, username FROM users WHERE user_id = :user_id", {"user_id": cur.lastrowid})
	user = cur.fetchone()
	
	conn.close()
	
	return users_row_dict(user)


def get_users():
	conn = get_connection()
	set_row_factory(conn)
	cur = conn.cursor()
	
	cur.execute("SELECT user_id, username, password FROM users")
	users = cur.fetchall()
	
	conn.close()
	
	return users_row_list(users)


def update_user(user_id, username):
	conn = get_connection()
	set_row_factory(conn)
	cur = conn.cursor()
	
	cur.execute("SELECT user_id, username FROM users WHERE user_id = :user_id", {"user_id": user_id})
	
	user = cur.fetchone()
	
	if user is None:
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
	
	cur.execute("SELECT user_id, username FROM users WHERE user_id = :user_id", {"user_id": user_id})
	
	user = cur.fetchone()
	
	if user is None:
		return NOT_FOUND
	
	cur.execute("DELETE FROM users WHERE user_id = :user_id", {"user_id": user_id})
	
	conn.commit()
	conn.close()
	
	return users_row_dict(user)