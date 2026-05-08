import sqlite3
import config

def get_connection(db_name):
	return sqlite3.connect(db_name)

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
			created_at TEXT DEFAULT (datetime('now'))
		)
	""")
	
	conn.commit()
	conn.close()
