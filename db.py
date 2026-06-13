import sqlite3
import config
import logging

logger = logging.getLogger(__name__)

def get_connection(db_name):
	try:
		return sqlite3.connect(db_name)
	except sqlite3.Error as e:
		logger.error(f"database error {e}")
		

def set_row_factory(conn):
	conn.row_factory = sqlite3.Row

def init_db(db_name):
	conn = get_connection(db_name)
	cur = conn.cursor()
	
	cur.execute("""
	CREATE TABLE IF NOT EXISTS tasks(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		title TEXT,
		done BOOLEAN DEFAULT FALSE,
		user_id INTEGER,
		archived BOOLEAN DEFAULT FALSE
	)
	""")
	
	cur.execute("""
		CREATE TABLE IF NOT EXISTS users(
			user_id INTEGER PRIMARY KEY AUTOINCREMENT,
			username TEXT,
			password TEXT
		)
	""")
	
	cur.execute("""
		CREATE TABLE IF NOT EXISTS comments(
			comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
			task_id INTEGER,
			user_id INTEGER,
			content TEXT,
			created_at TEXT DEFAULT (datetime('now')),
			deleted BOOLEAN DEFAULT FALSE
		)
	""")
	
	conn.commit()
	conn.close()