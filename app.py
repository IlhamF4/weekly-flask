from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def hello():
	return jsonify({"message": "hello world"})
	
tasks = []


#return json of tasks
def get_tasks():
	return jsonify(tasks)

#adding input from user to tasks
def add_task(title):
	tasks.append(title)
	return jsonify({"message": "added", "task": title})

@app.route("/tasks",methods=["GET","POST"])
def tasks_route():
	if request.method == "GET":
		return get_tasks()
	elif request.method == "POST":
		title = request.args.get("title")
		if not title:
			return {"error": "title required"},400
		return add_task(title)