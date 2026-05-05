from flask import request, jsonify
from werkzeug.exceptions import BadRequest, NotFound, Forbidden, Unauthorized
from utility.helpers import parse_json, check_positive_int, parse_token
from errors import *
from logic.auth import extract_user_id
from logic.comments import create_comment, get_comments, delete_comment

def get_user_id():
	user_id = extract_user_id()
	if  user_id == UNAUTHORIZED or user_id == NOT_FOUND:
		raise Unauthorized("invalid token")
	
	return user_id
	
	
#def handle_errors(value):
#	if value == NOT_FOUND:
#		raise NotFound("task not found")
#	if value == FORBIDDEN:
#		raise Forbidden("forbidden to modify")

def validate_content(value):
	if not isinstance(value, str):
		raise BadRequest("content must be a string")
	
	value = value.strip()
	
	
	if value == "":
		raise BadRequest("content cannot be empty")
		
	return value


def validate_create_comment(data):
	if "content" not in data:
		raise BadRequest("content is required")
		
	content = validate_content(data["content"])
	
	return {"content": content}


def register_comments_route(app):
	@app.route("/tasks/<task_id>/comments", methods=["POST"])
	def create_comment_route(task_id):
		user_id = get_user_id()
		data = parse_json()
		#validate input
		validated = validate_create_comment(data)
		content = validated["content"]
		
		#doing logic function post
		result = create_comment(user_id, task_id, content)
		
		#handle_errors(result)
		
		if result == NOT_FOUND:
			raise NotFound("task not found")
		if result == FORBIDDEN:
			raise Forbidden("forbidden to modify")
		
		#return response
		return jsonify({"data": result, "message": "comment created"}), 201
	
	
	@app.route("/tasks/<task_id>/comments", methods=["GET"])
	def get_comments_route(task_id):
		user_id = get_user_id()
		
		result = get_comments(user_id, task_id)
		
		#handle_errors(result)
		if result == NOT_FOUND:
			raise NotFound("task not found")
		if result == FORBIDDEN:
			raise Forbidden("forbidden to access")
			
		return jsonify({"data": result, "message": "comments"}), 200
		
	
	@app.route("/comments/<comment_id>", methods=["DELETE"])
	def delete_comment_route(comment_id):
		user_id = get_user_id()
		
		result = delete_comment(user_id, comment_id)
		
		#handle_errors(result)
		if result == NOT_FOUND:
			raise NotFound("comment not found")
		if result == FORBIDDEN:
			raise Forbidden("forbidden to modify")
		
		return jsonify({"data": result, "message": "comment deleted"})