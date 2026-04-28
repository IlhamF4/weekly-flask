from flask import jsonify, request
from werkzeug.exceptions import BadRequest, NotFound, Forbidden
from utility.helpers import parse_json, check_positive_int
from errors import NOT_FOUND, FORBIDDEN
from logic.auth import register_user
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

def validate_register(data):
	if "username" not in data:
		raise BadRequest("username is required")
	if "password" not in data:
		raise BadRequest("password is required")
		
	username = validate_username(data["username"])
	password = validate_password(data["password"])
	
	#password = hashed(password)
	
	return {"username": username, "password": password}
	

def register_auth_route(app):
	@app.route("/auth/register", methods=["POST"])
	def register_route():
		data = parse_json()
		
		validated = validate_register(data)
		
		username = validated["username"]
		password = validated["password"]
		
		result = register_user(username, password)
		
		return jsonify({"data": result, "message": "user registered"})
	