from flask import Flask, jsonify, request
from logic import get_tasks, add_task, update_task, delete_task

app = Flask(__name__)

@app.route("/")
def hello():
	return jsonify({"message": "hello world"})

@app.route("/tasks",methods=["GET","POST"])
def tasks_route():
	if request.method == "GET":
		return jsonify(get_tasks())
	elif request.method == "POST":
		title = request.args.get("title")
		if not title:
			return {"error": "title required"},400
		result = add_task(title)
		return jsonify({"message": "added", "task": result})

@app.route("/tasks/<int:task_id>",methods=["PUT"])
def task_update(task_id):
	title = request.args.get("title")
	if not title:
		return {"error": "title required"},400
		
	result = update_task(task_id,title)
	if result is None:
		return {"error": "id not found"},404
	else:
		return jsonify({"message": "updated", "task": result})

@app.route("/tasks/<int:task_id>",methods=["DELETE"])
def task_delete(task_id):
	result = delete_task(task_id)
	if result is None:
		return {"error": "id not found"},404
	else:
		return jsonify({"message": "deleted", "task": result})
		
if __name__ == "__main__":
	app.run(debug=True)