from flask import request, jsonify
from werkzeug.exceptions import BadRequest, NotFound, Forbidden, Unauthorized
import logging
from utility.helpers import *
from errors import *
from logic.tasks import add_task, get_tasks, update_task, delete_task, set_archive_task
from logic.auth import extract_user_id

logger = logging.getLogger(__name__)

def get_user_id():
	user_id = extract_user_id()
	if  user_id == UNAUTHORIZED or user_id == NOT_FOUND:
		raise Unauthorized("invalid token")
	
	return user_id
	
	
def handle_task_errors(value):
	if value == NOT_FOUND:
		raise NotFound("task not found")
	if value == FORBIDDEN:
		raise Forbidden("forbidden to modify task")


def validate_title(value):
	if not isinstance(value, str):
		raise BadRequest("title must be a string")
	
	title = value.strip()	
	if title == "":
		raise BadRequest("title cannot be empty")
		
	return title
	
	
def validate_done(value):
	if not isinstance(value, bool):
		raise BadRequest("done must be a boolean")
		
	return value
	

def validate_create_task(data):
	if "title" not in data:
		raise BadRequest("title is required")
		
	title = validate_title(data["title"])
	
	return {"title": title}


def validate_get_tasks():
	done = request.args.get("done")
	page = request.args.get("page")
	limit = request.args.get("limit")
	sort = request.args.get("sort")
	search = request.args.get("search")
	
	if done is not None:
		done = parse_bool(done)
		
	if search is not None:
		search = parse_search(search)
		
	if sort is not None:
		sort = parse_sort(sort)
	
	page = parse_page(page)
	limit = parse_limit(limit)
	
	return {"done": done, "search": search, "sort": sort, "page": page, "limit": limit}


def validate_update_task(data):
	if "title" not in data and "done" not in data:
		raise BadRequest("title or done is required")
	
	title = None
	done = None
	
	if "title" in data:
		title = validate_title(data["title"])
	if "done" in data:
		done = validate_done(data["done"])
		
	return {"title": title, "done": done}
	

def register_tasks_route(app):
	@app.route("/tasks", methods=["POST"])
	def create_task_route():
		user_id = get_user_id()
		
		data = parse_json()
		
		validated = validate_create_task(data)
		
		title = validated["title"]
		
		result = add_task(user_id, title)
		
		return jsonify({
			"data": result,
			"message": "Task created"
			}),201
	
	
	@app.route("/tasks", methods=["GET"])
	def get_tasks_route():
		user_id = get_user_id()
		
		validated = validate_get_tasks()
		
		done = validated["done"]
		search = validated["search"]
		sort = validated["sort"]
		page = validated["page"]
		limit = validated["limit"]
		
		result, total_rows = get_tasks(user_id, done, search, sort, page, limit)
		
		return jsonify({
			"data": result,
			"meta": {
				"page": page,
				"limit": limit,
				"page_count": len(result),
				"total_count": total_rows
			}
		}), 200
	
	
	@app.route("/tasks/<int:task_id>",methods=["PUT"])
	def update_task_route(task_id):
		user_id = get_user_id()
		
		data = parse_json()
		
		validated = validate_update_task(data)
		
		title = validated["title"]
		done = validated["done"]
		
		result = update_task(user_id, task_id, title,done)
		
		handle_task_errors(result)
		
		return jsonify({
			"data": result,
			"message": "Task updated"
			}), 200
	
	
	@app.route("/tasks/<int:task_id>", methods=["DELETE"])
	def delete_task_route(task_id):
		user_id = get_user_id()
		
		result = delete_task(user_id, task_id)
		
		handle_task_errors(result)
		
		return jsonify({
			"data": result,
			"message": "Task deleted"
		}), 200
		
		
	@app.route("/tasks/<int:task_id>/archive", methods=["PATCH"])
	def archive_route(task_id):
		user_id = get_user_id()
		
		result = set_archive_task(user_id, task_id, True)
		
		handle_task_errors(result)
			
		return jsonify({"data": result, "message": "task archived"})
	
	
	@app.route("/tasks/<int:task_id>/unarchive", methods=["PATCH"])
	def unarchive_route(task_id):
		user_id = get_user_id()
		
		result = set_archive_task(user_id, task_id, False)
		
		handle_task_errors(result)
			
		return jsonify({"data": result, "message": "task unarchived"})