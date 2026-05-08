import bcrypt
import random
import config
from db import get_connection, set_row_factory
from errors import *
from utility.helpers import parse_token
from logic.users import find_user

secret = ["Sauce123", "Nevermore", "LisaAnn"]

def row_to_dict(row):
	return {"user_id": row["user_id"], "username": row["username"]}
	

def extract_user_id():
	token = parse_token()
		
	parts = token.split(",")
	
	if len(parts) != 2:
		return UNAUTHORIZED
	
	head = parts[0]
	
	if head not in secret:
		return UNAUTHORIZED
	
	payload = parts[1]
	
	if not payload.isnumeric():
		return UNAUTHORIZED
	
	if find_user(payload) is None:
		return NOT_FOUND
	
	return int(payload)
	


def hash_password(password):
	password = password.encode('utf-8')
	
	salt = bcrypt.gensalt()
	
	hashed_pw = bcrypt.hashpw(password, salt)
	
	return hashed_pw


def verify_password(password, hashed_pw):
	password = password.encode('utf-8')
	
	result = bcrypt.checkpw(password, hashed_pw)
	
	return result


def gen_token(value):
	head = random.choice(secret)
	
	return f"{head},{value}"


#conflict with users file
def register_user(username, password):
	conn = get_connection(config.DB_NAME)
	set_row_factory(conn)
	cur = conn.cursor()
	
	cur.execute("SELECT username FROM users WHERE username = :username", {"username": username})
	
	user = cur.fetchone()
	
	if user is not None:
		return CONFLICT
	
	hash_pw = hash_password(password)
	
	cur.execute("INSERT INTO users (username, password) VALUES (:username, :password)", {"username": username, "password": hash_pw})
	conn.commit()
	
	cur.execute("SELECT user_id, username FROM users WHERE user_id = :user_id", {"user_id": cur.lastrowid})
	user = cur.fetchone()
	
	conn.close()
	
	return row_to_dict(user)


def login_user(username, password):
	conn = get_connection(config.DB_NAME)
	set_row_factory(conn)
	cur = conn.cursor()

	cur.execute("SELECT user_id, username, password FROM users WHERE username = :username", {"username": username})
	
	user = cur.fetchone()
	
	if user is None:
		return NOT_FOUND
	
	hashed_pw = user["password"]
	
	result = verify_password(password, hashed_pw)
	
	if not result:
		return UNAUTHORIZED
	
	token = gen_token(user["user_id"])
	
	return {"user": row_to_dict(user), "token": token}