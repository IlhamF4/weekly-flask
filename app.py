from flask import Flask, jsonify, request
from werkzeug.exceptions import BadRequest
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
		return jsonify({"error": "content must be json"}),400
	
	try:
		data = request.get_json()
	except BadRequest:
		return jsonify({"error": "Invalid json"}),400
	
	if data == {}:
		return jsonify({"error": "this is empty body"}),400
	return data

@app.route("/tasks",methods=["POST"])
def create_task_route():
	data = access_json()
	if "title" not in data:
		return jsonify({"error": "title required"}),400
	
	title = data["title"]
	if title == "":
		return jsonify({"error": "title cannot be empty"}),400
		
	result = add_task(title)
	return jsonify({"message": "added", "task": result})

@app.route("/tasks/<int:task_id>",methods=["PUT"])
def update_task_route(task_id):
	title = None
	done = None
	
	data = access_json()
	if "title" not in data and "done" not in data:
		return jsonify({"error": "please input title or done"})
	
	if "title" in data:
		title = data["title"]
	if "done" in data:
		done = is_bool(data)
	
	result = update_task(task_id,title,done)
	if result is None:
		return jsonify({"error": "id not found"}),404
	
	return jsonify({"message": "updated", "task": result})

def is_bool(data):
	value = data["done"].lower()
	
	if value == "true":
		return True
	elif value == "false":
		return False
	else:
		return jsonify({"error": "value of done must be either true or false"}),400

@app.route("/tasks/<int:task_id>",methods=["DELETE"])
def delete_task_route(task_id):
	result = delete_task(task_id)
	if result is None:
		return jsonify({"error": "id not found"}),404
	
	return jsonify({"message": "deleted", "task": result})
		
if __name__ == "__main__":
	app.run(debug=True)