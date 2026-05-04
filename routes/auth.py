from flask import jsonify, request
from werkzeug.exceptions import BadRequest, NotFound, Forbidden, Conflict, Unauthorized
from utility.helpers import parse_json, check_positive_int
from errors import *
from logic.auth import register_user, login_user, hash_password, verify_password
from logic.users import find_user
from routes.users import validate_username

def get_user_id():
	if "X-User-Id" not in request.headers:
		raise BadRequest("X-User-Id must exist in header")
		
	user_id = request.headers.get("X-User-Id")
	
	user_id = validate_user_id(user_id)
	
	return user_id


def validate_user_id(user_id):
	if not check_positive_int(user_id):
		raise BadRequest("input must be a positive integer")
	
	user_id = int(user_id)
	
	if find_user(user_id) == NOT_FOUND:
		raise NotFound("user not found")
	
	return user_id


def validate_password(password):
	if not isinstance(password, str):
		raise BadRequest("password must be a string")
	
	if len(password) < 8:
		raise BadRequest("password cannot be less than 8 character")
	
	return password

def validate_data(data):
	if "username" not in data:
		raise BadRequest("username is required")
	if "password" not in data:
		raise BadRequest("password is required")
		
	username = validate_username(data["username"])
	
	password = validate_password(data["password"])
	
	return {"username": username, "password": password}
	

def register_auth_route(app):
	@app.route("/auth/register", methods=["POST"])
	def register_route():
		data = parse_json()
		
		validated = validate_data(data)
		
		username = validated["username"]
		password = validated["password"]
		
		result = register_user(username, password)
		
		if result == CONFLICT:
			raise Conflict("username already exist")
		
		return jsonify({"data": result, "message": "user registered"})
		
	@app.route("/auth", methods=["GET"])
	def examp():
		result = register_user("wong", "1234")
		return jsonify(result)
	
	
	@app.route("/auth/login", methods=["POST"])
	def login_route():
		data = parse_json()
		validated = validate_data(data)
		
		username = validated["username"]
		password = validated["password"]
		
		result = login_user(username, password)
		
		if result == NOT_FOUND:
			raise NotFound("username not found")
		
		if result == UNAUTHORIZED:
			raise Unauthorized("password is incorrect")
		
		return jsonify({"data": result["user"], "token": result["token"], "message": "login successful"})