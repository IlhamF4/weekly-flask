from flask import request, jsonify
from werkzeug.exceptions import BadRequest, NotFound, Forbidden, Unauthorized
import logging
from utility.helpers import *
from errors import *
from logic.auth import extract_user_id
from logic.comments import add_comment, get_comments, delete_comment, restore_comment

logger = logging.getLogger(__name__)

def get_user_id():
	user_id = extract_user_id()
	if  user_id == UNAUTHORIZED or user_id == NOT_FOUND:
		raise Unauthorized("invalid token")
	
	return user_id
	

def handle_tasks_errors(value):
	if value == NOT_FOUND:
		logger.info("task not found")
		raise NotFound("task not found")
	if value == FORBIDDEN:
		logger.warning("Unauthorized action detected")
		raise Forbidden("forbidden to modify task")


def handle_comments_errors(value):
	if value == NOT_FOUND:
		raise NotFound("comment not found")
	if value == FORBIDDEN:
		raise Forbidden("forbidden to modify comment")
	

def validate_content(value):
	if not isinstance(value, str):
		raise BadRequest("content must be a string")
	
	value = value.strip()
	
	
	if value == "":
		raise BadRequest("content cannot be empty")
		
	return value
	
	
def validate_include_deleted(value):
	if value is None:
		return False
	
	return parse_bool(value)


def validate_create_comment(data):
	if "content" not in data:
		raise BadRequest("content is required")
		
	content = validate_content(data["content"])
	
	return {"content": content}


def validate_get_comments():
	include_deleted = request.args.get("deleted")
	page = request.args.get("page")
	limit = request.args.get("limit")
	
	include_deleted = validate_include_deleted(include_deleted)
	
	page = parse_page(page)
	limit = parse_limit(limit)
	
	return {"deleted": include_deleted, "page": page, "limit": limit}


def register_comments_route(app):
	@app.route("/tasks/<int:task_id>/comments", methods=["POST"])
	def create_comment_route(task_id):
		user_id = get_user_id()
		data = parse_json()
		
		validated = validate_create_comment(data)
		content = validated["content"]
		
		result = add_comment(user_id, task_id, content)
		
		handle_tasks_errors(result)
		
		return jsonify({"data": result, "message": "comment created"}), 201
	
	
	@app.route("/tasks/<int:task_id>/comments", methods=["GET"])
	def get_comments_route(task_id):
		user_id = get_user_id()
		
		validated = validate_get_comments()
		
		include_deleted = validated["deleted"]
		page = validated["page"]
		limit = validated["limit"]
		
		result, total_rows= get_comments(user_id, task_id, include_deleted, page, limit)
		
		handle_tasks_errors(result)

		return jsonify({
			"data": result, 
			"meta": {
				"page": page, 
				"limit": limit, 
				"page count": len(result), 
				"total count": total_rows
			}
		}), 200
		
	
	@app.route("/comments/<int:comment_id>", methods=["DELETE"])
	def delete_comment_route(comment_id):
		user_id = get_user_id()
		
		result = delete_comment(user_id, comment_id)
		
		handle_comments_errors(result)

		return jsonify({"data": result, "message": "comment deleted"}), 200
		
	
	@app.route("/comments/<int:comment_id>", methods=["PATCH"])
	def restore_comment_route(comment_id):
		user_id = get_user_id()
		
		result = restore_comment(user_id, comment_id)
		
		handle_comments_errors(result)
		
		return jsonify({"data": result, "message": "comment restored"}), 200