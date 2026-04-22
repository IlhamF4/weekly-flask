from flask import Flask, jsonify, request
from logic import get_tasks, add_task, update_task, delete_task

app = Flask(__name__)

@app.route("/")
def hello():
	return jsonify({"message": "hello world"})

@app.route("/tasks",methods=["GET"])
def get_tasks_route():
	return jsonify(get_tasks())

@app.route("/tasks",methods=["POST"])
def create_task_route():
	title = request.args.get("title")
	if not title:
		return jsonify({"error": "title required"}),400
		
	result = add_task(title)
	return jsonify({"message": "added", "task": result})

@app.route("/tasks/<int:task_id>",methods=["PUT"])
def update_task_route(task_id):
	title = request.args.get("title")
	done = request.args.get("done")
	if title is None and done is None:
		return jsonify({"error": "no data provided"}),400
	
	if done is not None:
		done = done.lower() == "true"
	print(title)
	print(done)
	result = update_task(task_id,title,done)
	if result is None:
		return jsonify({"error": "id not found"}),404
	
	return jsonify({"message": "updated", "task": result})

@app.route("/tasks/<int:task_id>",methods=["DELETE"])
def delete_task_route(task_id):
	result = delete_task(task_id)
	if result is None:
		return jsonify({"error": "id not found"}),404
	
	return jsonify({"message": "deleted", "task": result})
		
if __name__ == "__main__":
	app.run(debug=True)