import pytest
from tests.prepare_env import *
from logic.tasks import validate_task_access, is_task_archived, set_archive_task, add_task, delete_task
from logic.comments import add_comment
from errors import *

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
	conn.close()
	
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
	
	result = set_archive_task(user["user_id"], task["id"], True)
	
	assert result["archived"] is True


def test_add_comment_on_archived_task_return_forbidden():
	clear_tables()
	
	user, task = prepare_data()
	
	set_archive_task(user["user_id"], task["id"], True)
	
	result = add_comment(user["user_id"], task["id"], "test")
	
	assert result == FORBIDDEN
	

def test_delete_task_return_forbidden():
	clear_tables()
	
	user, task = prepare_data()
	
	result = delete_task((user["user_id"] + 1), task["id"])
	
	assert result == FORBIDDEN