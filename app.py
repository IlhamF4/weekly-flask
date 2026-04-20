from flask import Flask, jsonify, request
from logic import get_tasks, add_task

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
		return jsonify(add_task(title))

if __name__ == "__main__":
	app.run(debug=True)