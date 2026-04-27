from flask import Flask, jsonify, request
from werkzeug.exceptions import BadRequest, NotFound, HTTPException
from logic import get_tasks, add_task, update_task, delete_task, init_db, check_user, add_user, get_users

app = Flask(__name__)

#Helper functions
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


# Helper users
def validate_user_id(value):
	if not isinstance(value, int):
		raise BadRequest("invalid type")
	
	if value <= 0:
		raise BadRequest("user id must be a positive integer")
	
	if check_user(value) is None:
		raise NotFound("user not found")
	
	return value


# Helper tasks
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
		
		
def validate_int(value):
	if value is None:
		return None
	
	if not value.isdecimal() or value == "0":
		raise BadRequest("input must be a positive integer")
		
	return int(value)
		
		
def parse_page(value):
	if value is None:
		return 1
	
	return validate_int(value)
	

def parse_limit(value):
	if value is None:
		return 10
	
	return validate_int(value)


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
	
# Validation users
def get_user_id():
	if "X-User-Id" not in request.headers:
		raise BadRequest("X-User-Id must exist in header")
		
	user_id = request.headers.get("X-User-Id")
	
	user_id = validate_user(user_id)
	
	return user_id


def validate_username(value):
	if value is None:
		raise BadRequest("username is required")
	
	value = value.strip()
	
	if value == "":
		raise BadRequest("username cannot be empty")
	
	return value

def validate_add_user():
	username = request.args.get("username")
	
	validated_username = validate_username(username)
	
	return {"username": validated_username}

# Validation of tasks route
def validate_create_task(data):
	if "title" not in data:
		raise BadRequest("title is required")
		
	title = validate_title(data["title"])
	
	return {"title": title}


def validate_get_tasks():
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
	
	return {"done": done, "search": search, "sort": sort, "page": page, "limit": limit}


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
	user_id = get_user_id()
	return jsonify({"message": "hello world", "data": user_id})


# Users area
@app.route("/users", methods=["POST"])
def add_user_route():
	validated = validate_add_user()
	
	user = add_user(validated["username"])
	
	return jsonify({"data": user, "message": "user added"})


@app.route("/users", methods=["GET"])
def get_users_route():
	users = get_users()
	
	return jsonify({
		"data": users,
		"count": len(users)
	})


@app.route("/users", methods=["PUT"])
def update_user_route():
	pass


@app.route("/users", methods=["DELETE"])
def delete_user_route():
	pass


#Tasks area
@app.route("/tasks", methods=["POST"])
def create_task_route():
	data = parse_json()
	
	validated = validate_create_task(data)
	
	title = validated["title"]
	
	result = add_task(title)
	
	return jsonify({
		"data": result,
		"message": "Task created"
		}),201


@app.route("/tasks", methods=["GET"])
def get_tasks_route():
	validated = validate_get_tasks()
	
	done = validated["done"]
	search = validated["search"]
	sort = validated["sort"]
	page = validated["page"]
	limit = validated["limit"]
	
	result = get_tasks(done, search, sort, page, limit)
	
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
	
	title = validated["title"]
	done = validated["done"]
	
	result = update_task(task_id, title,done)
	
	if result is None:
		raise NotFound("task not found")
	
	return jsonify({
		"data": result,
		"message": "Task updated"
		}), 200


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task_route(task_id):
	result = delete_task(task_id)
	
	if result is None:
		raise NotFound("task not found")
	
	return jsonify({
		"data": result,
		"message": "Task deleted"
	}), 200
	

@app.errorhandler(HTTPException)
def handle_http_exception(e):
			return jsonify({
				"error": e.description
			}), e.code
			

init_db()

if __name__ == "__main__":
	app.run(debug=True)