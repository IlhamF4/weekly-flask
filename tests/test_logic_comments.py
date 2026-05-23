import pytest
from errors import *
from tests.prepare_env import *
from logic.comments import add_comment, get_comments, delete_comment, restore_comment

def test_add_comment_to_other_user_task():
	clear_tables()
	
	user, task = prepare_data()
	
	result = add_comment((user["user_id"] + 1), task["id"],"test")
	
	assert result == FORBIDDEN
	
	
def test_add_comment_to_nonexistent_task():
	clear_tables()
	
	user, task = prepare_data()
	
	result = add_comment(user["user_id"] , (task["id"] + 1),"test")
	
	assert result == NOT_FOUND
	
	
def test_add_comment_return_added_comment():
	clear_tables()
	
	user, task = prepare_data()
	
	result = add_comment(user["user_id"], task["id"],"test")
	
	assert result["content"] == "test"


def test_get_comments_return_comments():
	clear_tables()
	
	user, task = prepare_data()
	
	comment = add_comment(user["user_id"], task["id"], "test")
	
	result = get_comments(user["user_id"], task["id"])
	
	assert result[0]["content"] == "test"
	

def test_deleted_comments_hidden_by_default():
	clear_tables()
	
	user, task = prepare_data()
	
	comment = add_comment(user["user_id"], task["id"], "test")
	
	delete_comment(user["user_id"], comment["comment_id"])
	
	result = get_comments(user["user_id"], task["id"])
	
	assert result == []


def test_deleted_comments_hidden_when_include_deleted_is_false():
	clear_tables()
	
	user, task = prepare_data()
	
	comment = add_comment(user["user_id"], task["id"], "test")
	
	delete_comment(user["user_id"], comment["comment_id"])
	
	result = get_comments(user["user_id"], task["id"], False)
	
	assert result == []
	

def test_deleted_comment_show_on_get_comments():
	clear_tables()
	
	user, task = prepare_data()
	
	conn, cur = db_connection()
	
	comment = add_comment(user["user_id"], task["id"], "test")
	
	delete_comment(user["user_id"], comment["comment_id"])
	
	result = get_comments(user["user_id"], task["id"], True)
	
	assert result[0]["content"] == "test"
	

def test_page_above_last_comment_return_empty_list():
	clear_tables()
	
	user, task = prepare_data()
	
	comment = add_comment(user["user_id"], task["id"], "test")
	
	result = get_comments(user["user_id"], task["id"], 2, 10)
	
	assert result == []
	

def test_delete_comment_return_success():
	clear_tables()
	
	user, task = prepare_data()
	
	comment = add_comment(user["user_id"], task["id"], "test")
	
	result = delete_comment(user["user_id"], comment["comment_id"])
	
	assert result["deleted"] is True


def test_deleted_comment_return_not_found():
	clear_tables()
	
	user, task = prepare_data()
	
	comment = add_comment(user["user_id"], task["id"], "test")
	
	delete_comment(user["user_id"], comment["comment_id"])
	
	result = delete_comment(user["user_id"], comment["comment_id"])
	
	assert result == NOT_FOUND
	

def test_restore_comment_successful():
	clear_tables()
	
	user, task = prepare_data()
	
	comment = add_comment(user["user_id"], task["id"], "test")
	
	delete_comment(user["user_id"], comment["comment_id"])
	
	result = restore_comment(user["user_id"], comment["comment_id"])
	
	assert result["deleted"] is False