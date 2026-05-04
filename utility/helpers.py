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