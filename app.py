from flask import Flask, jsonify, request
from werkzeug.exceptions import BadRequest, NotFound
from logic import get_tasks, add_task, update_task, delete_task

app = Flask(__name__)

def parse_json():
	if not request.is_json:
		raise BadRequest("content must be json")
	
	try:
		data = request.get_json()
	except BadRequest:
		raise BadRequest("Invalid json")
	
	if data is None:
		raise BadRequest("request body is required")
	
	if data == {}:
		raise BadRequest("request body cannot be empty")
		
	return data
	
	
def validate_title(value):
	if not isinstance(value,str):
		raise BadRequest("title must be a string")
	
	title = value.strip()	
	if title == "":
		raise BadRequest("title cannot be empty")
		
	return title


def validate_bool(value):
	if value is None:
		return None
		
	value = value.lower()
	
	if value == "true":
		return True
	elif value == "false":
		return False
	else:
		raise BadRequest("Input must be either true or false")
		
		
def validate_int(value):
	if value is None:
		return None
	
	if not value.isdecimal() or value == "0":
		raise BadRequest("input must be a positive integer")
		
	return int(value)
		
def validate_page(value):
	if value is None:
		return 1
	
	return validate_int(value)
	

def validate_limit(value):
	if value is None:
		return 10
	
	return validate_int(value)
	
	
def validate_done(value):
	if not isinstance(value,bool):
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
	
	if done is not None:
		done = validate_bool(done)
	
	page = validate_page(page)
	limit = validate_limit(limit)
	
	return {"done": done, "page": page, "limit": limit}


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


@app.route("/")
def hello():
	return jsonify({"message": "hello world"})


@app.route("/tasks", methods=["GET"])
def get_tasks_route():
	validated = validate_get_tasks()
	done = validated["done"]
	page = validated["page"]
	limit = validated["limit"]
	
	tasks = get_tasks(done, page, limit)
	
	return jsonify({"tasks": tasks}),200


@app.route("/tasks", methods=["POST"])
def create_task_route():
	data = parse_json()
	
	validated = validate_create_task(data)
	title = validated["title"]
	
	result = add_task(title)
	
	return jsonify({"message": "added", "task": result}),201


@app.route("/tasks/<int:task_id>",methods=["PUT"])
def update_task_route(task_id):
	data = parse_json()
	
	validated = validate_update_task(data)
	title = validated["title"]
	done = validated["done"]
	
	result = update_task(task_id, title,done)
	
	if result is None:
		raise NotFound("task not found")
	
	return jsonify({"message": "updated", "task": result}),200


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task_route(task_id):
	result = delete_task(task_id)
	
	if result is None:
		raise NotFound("task not found")
	
	return jsonify({"message": "deleted", "task": result}),200
	
			
if __name__ == "__main__":
	app.run(debug=True)