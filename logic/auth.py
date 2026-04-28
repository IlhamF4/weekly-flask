from db import get_connection, set_row_factory

def auth_row_dict(row):
	return {"user_id": row["user_id"], "username": row["username"]}

def register_user(username, password):
	conn = get_connection()
	set_row_factory(conn)
	cur = conn.cursor()
	
	cur.execute("INSERT INTO users (username, password) VALUES (:username, :password)", {"username": username, "password": password})
	conn.commit()
	
	cur.execute("SELECT user_id, username FROM users WHERE user_id = :user_id", {"user_id": cur.lastrowid})
	user = cur.fetchone()
	
	conn.close()
	
	return auth_row_dict(user)


def hashed(password):
	password = password.encode('utf-8')
	salt = bcrypt.gensalt()
	
	hashed_pw = bcrypt.hashpw(password, salt)
	
	return hashed_pw


#def check_pw(password, user_id):
#	password = password.encode('utf-8')
#	hashed_pw = get_password(user_id)
#	
#	if bcrypt.checkpw(password, hashed_pw):
#		return True
#	else:
#		return False
