import sqlite3
import config
import logging
import psycopg

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
		task_id INTEGER PRIMARY KEY AUTOINCREMENT,
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
	

def get_connection_postgre():
	conn = psycopg.connect(conninfo=config.DB_URL, user="admin", password="admin123")
	cur = conn.cursor()
	return conn, cur
	

def init_db_postgre():
	conn, cur = get_connection_postgre()

	cur.execute("""
		CREATE TABLE IF NOT EXISTS tasks (
			task_id SERIAL PRIMARY KEY,
			title VARCHAR(50) NOT NULL,
			done BOOLEAN DEFAULT FALSE,
			user_id INT,
			archived BOOLEAN DEFAULT FALSE
		)
	""")

	cur.execute("""
		CREATE TABLE IF NOT EXISTS users (
			user_id SERIAL PRIMARY KEY,
			username VARCHAR(50) UNIQUE NOT NULL,
			password VARCHAR(50) NOT NULL
		)
	""")

	cur.execute("""
		CREATE TABLE IF NOT EXISTS comments (
			comment_id SERIAL PRIMARY KEY,
			task_id INT,
			user_id INT,
			content TEXT,
			created_at TIMESTAMP NOT NULL,
			deleted BOOLEAN DEFAULT FALSE
		)
	""")
	conn.commit()
	conn.close()

print(init_db_postgre())
	
#change config.DB_NAME to inside db .py so that it doesnt hardcoded inside funvtion