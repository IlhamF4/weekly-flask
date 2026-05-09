import config
from db import get_connection, init_db, set_row_factory
from logic.users import add_user
from logic.tasks import add_task

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