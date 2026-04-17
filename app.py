from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def hello():
	return jsonify({"message": "hello world"})
	
tasks = []
@app.route("/tasks")
def get_tasks():
	return jsonify(tasks)