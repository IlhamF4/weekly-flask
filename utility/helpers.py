from flask import request
from werkzeug.exceptions import BadRequest, Unauthorized

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

# String -> Boolean
def check_positive_int(value):
	if value is None:
		return None
	
	return value.isdecimal() and value != "0"


def parse_token():
	token = request.headers.get("Authorization")
	
	if token is None:
		raise Unauthorized("token is required")
	
	token = token.strip()
	
	if token == "":
		raise Unauthorized("token cannot be empty")
	
	return token
	

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
		
		
def parse_page(value):
	if value is None:
		return 1
	
	if not check_positive_int(value):
		raise BadRequest("input must be a positive integer")
	
	return int(value)
	

def parse_limit(value):
	if value is None:
		return 10
	
	if not check_positive_int(value):
		raise BadRequest("input must be a positive integer")
	
	return int(value)


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