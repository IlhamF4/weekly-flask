from flask import request, jsonify
from werkzeug.exceptions import BadRequest, NotFound, Forbidden, Unauthorized
from utility.helpers import parse_json, check_positive_int, parse_token
from errors import *
from logic.tasks import add_task, get_tasks, update_task, delete_task
#from logic.users import find_user
from logic.auth import extract_user_id
#from routes.auth import get_user_id


def get_user_id():
	user_id = extract_user_id()
	if  user_id == UNAUTHORIZED or user_id == NOT_FOUND:
		raise Unauthorized("invalid token")
	
	return user_id
	
	
def parse_bool(value):
	if value is None:
		return None
		
	value = value.lower()
	
	if value == "true":
		return True
	elif value == "false":
		return False
	else:
		raise BadRequest("Input must be either true or false")
		
		
def parse_page(value):
	if value is None:
		return 1
	
	if not check_positive_int(value):
		raise BadRequest("input must be a positive integer")
	
	return int(value)
	

def parse_limit(value):
	if value is None:
		return 10
	
	if not check_positive_int(value):
		raise BadRequest("input must be a positive integer")
	
	return int(value)


def parse_sort(value):
	if value is None:
		return None
	
	value = value.lower()
	
	if value == "asc":
		return "ASC"
	elif value == "desc":
		return "DESC"
	else:
		raise BadRequest("input must be either asc or desc")
		

def parse_search(value):
	if value is None:
		return None
	
	value = value.strip()
	
	if value == "":
		raise BadRequest("search cannot be empty")
	
	return value


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
	user_id = get_user_id()
		
	if "title" not in data:
		raise BadRequest("title is required")
		
	title = validate_title(data["title"])
	
	return {"user_id": user_id, "title": title}


def validate_get_tasks():
	user_id = get_user_id()
		
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
	
	return {"user_id": user_id, "done": done, "search": search, "sort": sort, "page": page, "limit": limit}


def validate_update_task(data):
	user_id = get_user_id()
		
	if "title" not in data and "done" not in data:
		raise BadRequest("title or done is required")
	
	title = None
	done = None
	
	if "title" in data:
		title = validate_title(data["title"])
	if "done" in data:
		done = validate_done(data["done"])
		
	return {"user_id": user_id, "title": title, "done": done}

def validate_delete_task():
	user_id = get_user_id()
	
	return {"user_id": user_id}
	

def register_tasks_route(app):
	@app.route("/tasks", methods=["POST"])
	def create_task_route():
		data = parse_json()
		
		validated = validate_create_task(data)
		
		title = validated["title"]
		user_id = validated["user_id"]
		
		result = add_task(user_id, title)
		
		return jsonify({
			"data": result,
			"message": "Task created"
			}),201
	
	
	@app.route("/tasks", methods=["GET"])
	def get_tasks_route():
		validated = validate_get_tasks()
		
		user_id = validated["user_id"]
		done = validated["done"]
		search = validated["search"]
		sort = validated["sort"]
		page = validated["page"]
		limit = validated["limit"]
		
		result = get_tasks(user_id, done, search, sort, page, limit)
		
		return jsonify({
			"data": result,
			"meta": {
				"page": page,
				"limit": limit,
				"count": len(result)
			}
		}), 200
	
	
	@app.route("/tasks/<int:task_id>",methods=["PUT"])
	def update_task_route(task_id):
		data = parse_json()
		
		validated = validate_update_task(data)
		
		user_id = validated["user_id"]
		title = validated["title"]
		done = validated["done"]
		
		result = update_task(user_id, task_id, title,done)
		
		if result == FORBIDDEN:
			raise Forbidden("forbidden to modify task")
		
		if result == NOT_FOUND:
			raise NotFound("task not found")
		
		return jsonify({
			"data": result,
			"message": "Task updated"
			}), 200
	
	
	@app.route("/tasks/<int:task_id>", methods=["DELETE"])
	def delete_task_route(task_id):
		validated = validate_delete_task()
		
		user_id = validated["user_id"]
		result = delete_task(user_id, task_id)
		
		if result == FORBIDDEN:
			raise Forbidden("forbidden to modify task")
		
		if result == NOT_FOUND:
			raise NotFound("task not found")
		
		return jsonify({
			"data": result,
			"message": "Task deleted"
		}), 200