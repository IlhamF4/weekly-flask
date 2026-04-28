import sqlite3

def get_connection():
	return sqlite3.connect("task.db")

def set_row_factory(conn):
	conn.row_factory = sqlite3.Row

def init_db():
	conn = get_connection()
	cur = conn.cursor()
	
	cur.execute("""
	CREATE TABLE IF NOT EXISTS tasks(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		title TEXT,
		done BOOLEAN,
		user_id INTEGER
	)
	""")
	
	cur.execute("""
		CREATE TABLE IF NOT EXISTS users(
			user_id INTEGER PRIMARY KEY AUTOINCREMENT,
			username TEXT,
			password TEXT
		)
	""")
	
	conn.commit()
	conn.close()