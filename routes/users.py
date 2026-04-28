from flask import request, jsonify
from werkzeug.exceptions import BadRequest, NotFound, Forbidden
from errors import NOT_FOUND
from logic.users import find_user, add_user, get_users, update_user, delete_user
from utility.helpers import parse_json

def validate_username(username):
	if not isinstance(username, str):
		raise BadRequest("username must be a string")
	
	if not username.isalnum():
		raise BadRequest("username cannot be  special character")
	
	if len(username) < 4 or len(username) > 8:
		raise BadRequest("username must be 4-8 character")
	
	username = username.strip()
	
	if username == "":
		raise BadRequest("username cannot be empty")
	
	return username

def validate_add_user(data):
	if "username" not in data:
		raise BadRequest("username is required")
	
	username = validate_username(data["username"])
	
	return {"username": username}


def validate_update_user(user_id, data):
	if find_user(user_id) == NOT_FOUND:
		raise NotFound("user_id not found")
	
	if "username" not in data:
		raise BadRequest("username is required")
	
	username = validate_username(data["username"])
	
	return {"username": username}

def register_users_route(app):
	@app.route("/users", methods=["POST"])
	def add_user_route():
		data = parse_json()
		
		validated = validate_add_user(data)
		
		result = add_user(validated["username"])
		
		return jsonify({"data": result, "message": "user added"})
	
	
	@app.route("/users", methods=["GET"])
	def get_users_route():
		result = get_users()
		
		return jsonify({
			"data": result,
			"count": len(result)
		})
	
	
	@app.route("/users/<user_id>", methods=["PUT"])
	def update_user_route(user_id):
		data = parse_json()
		
		validated = validate_update_user(user_id, data)
		
		username = validated["username"]
		
		result = update_user(user_id, username)
		
		if result == NOT_FOUND:
			raise NotFound("user not found")
		
		return jsonify({"data": result, "message": "user updated"})
	
	
	@app.route("/users/<user_id>", methods=["DELETE"])
	def delete_user_route(user_id):
		result = delete_user(user_id)
		
		if result == NOT_FOUND:
			raise NotFound("user not found")
		
		return jsonify({"data": result, "message": "user deleted"})
	