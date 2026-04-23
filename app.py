from flask import Flask, jsonify, request
from werkzeug.exceptions import BadRequest, NotFound
from logic import get_tasks, add_task, update_task, delete_task

app = Flask(__name__)

@app.route("/")
def hello():
	return jsonify({"message": "hello world"})

@app.route("/tasks",methods=["GET"])
def get_tasks_route():
	return jsonify(get_tasks())
	
def access_json():
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

@app.route("/tasks",methods=["POST"])
def create_task_route():
	data = access_json()
	if "title" not in data:
		raise BadRequest("title is required")
	
	if not isinstance(data["title"],str):
		raise BadRequest("title must be string")
	
	title = data["title"].strip()	
	if title == "":
		raise BadRequest("title cannot be empty")
		
	result = add_task(title)
	return jsonify({"message": "added", "task": result})

@app.route("/tasks/<int:task_id>",methods=["PUT"])
def update_task_route(task_id):
	title = None
	done = None
	
	data = access_json()
	if "title" not in data and "done" not in data:
		raise BadRequest("title or done is required")
	
	if "title" in data:
		if not isinstance(data["title"],str):
			raise BadRequest("title must be string")
		
		title = data["title"].strip()
		if title == "":
			raise BadRequest("title cannot be empty")
			
	if "done" in data:
		if not isinstance(data["done"],bool):
			raise BadRequest("done must be boolean")
		done = data["done"]
	
	result = update_task(task_id,title,done)
	if result is None:
		raise NotFound("task not found")
	
	return jsonify({"message": "updated", "task": result})


@app.route("/tasks/<int:task_id>",methods=["DELETE"])
def delete_task_route(task_id):
	result = delete_task(task_id)
	if result is None:
		raise NotFound("task not found")
	
	return jsonify({"message": "deleted", "task": result})
		
if __name__ == "__main__":
	app.run(debug=True)