import pytest
import sqlite3
import config
from logic.tasks import validate_task_access, is_task_archived, set_archive_task, add_task, delete_task
from logic.users import add_user
from logic.comments import add_comment
from db import get_connection, set_row_factory, init_db
from errors import *

config.DB_NAME = "test.db"

init_db(config.DB_NAME)

def db_connection():
	conn = get_connection(config.DB_NAME)
	set_row_factory(conn)
	cur = conn.cursor()
	
	return conn, cur
	

def clear_tables():
	conn, cur = db_connection()
	
	cur.execute("DELETE FROM tasks")
	cur.execute("DELETE FROM users")
	cur.execute("DELETE FROM comments")
	conn.commit()
	
	conn.close()

""" Now we have in table users row [1, "linda", ""], in table tasks row [1, "learning", false]"""
def prepare_data():
	user_id = add_user("linda")
	task = add_task(user_id["user_id"], "learning")
	
	return user_id, task

def test_validate_task_access_return_forbidden():
	clear_tables()
	
	user, task= prepare_data()
	
	conn, cur = db_connection()
	
	result = validate_task_access(cur, (user["user_id"] + 1), task["id"]) 
	conn.close()
	
	assert result == FORBIDDEN


def test_validate_task_access_return_not_found():
	clear_tables()
	
	user, task = prepare_data()
	
	conn, cur = db_connection()
	
	result = validate_task_access(cur, user["user_id"], (task["id"] + 1))
	conn.close()
	
	assert result == NOT_FOUND
	

def test_validate_task_access_return_success():
	clear_tables()
	
	user, task = prepare_data()
	
	conn, cur = db_connection()
	
	result = validate_task_access(cur, user["user_id"], task["id"])
	
	assert result["id"] == task["id"]
	

def test_is_task_archived_return_false():
	clear_tables()
	
	user, task = prepare_data()
	
	conn, cur = db_connection()
	
	result =  is_task_archived(cur, task["id"])
	
	conn.close()
	
	assert result is False


def test_set_archive_task_archived():
	clear_tables()
	
	user, task = prepare_data()
	
	conn, cur = db_connection()
	
	result = set_archive_task(user["user_id"], task["id"], True)
	
	assert result["archived"] is True


def test_add_comment_on_archived_task_return_forbidden():
	clear_tables()
	
	user, task = prepare_data()
	
	conn, cur = db_connection()
	
	set_archive_task(user["user_id"], task["id"], True)
	
	result = add_comment(user["user_id"], task["id"], "test")
	
	assert result == FORBIDDEN
	

def test_delete_task_return_forbidden():
	clear_tables()
	
	user, task = prepare_data()
	
	conn, cur = db_connection()
	
	result = delete_task((user["user_id"] + 1), task["id"])
	
	assert result == FORBIDDEN