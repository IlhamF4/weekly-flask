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
	
def validate_done(value):
	if not isinstance(value,bool):
		raise BadRequest("done must be a boolean")
		
	return value
	
	
def validate_create_task(data):
	if "title" not in data:
		raise BadRequest("title is required")
		
	title = validate_title(data["title"])
	
	return {"title": title}


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
	return jsonify(get_tasks())


@app.route("/tasks", methods=["POST"])
def create_task_route():
	data = parse_json()
	
	validated = validate_create_task(data)
	title = validated["title"]
	
	result = add_task(title)
	
	return jsonify({"message": "added", "task": result})


@app.route("/tasks/<int:task_id>",methods=["PUT"])
def update_task_route(task_id):
	data = parse_json()
	
	validated = validate_update_task(data)
	title = validated["title"]
	done = validated["done"]
	
	result = update_task(task_id, title,done)
	
	if result is None:
		raise NotFound("task not found")
	
	return jsonify({"message": "updated", "task": result})


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task_route(task_id):
	result = delete_task(task_id)
	
	if result is None:
		raise NotFound("task not found")
	
	return jsonify({"message": "deleted", "task": result})
	
			
if __name__ == "__main__":
	app.run(debug=True)