from flask import Flask, jsonify
from werkzeug.exceptions import BadRequest, NotFound, HTTPException, Forbidden
from routes.users import register_users_route
from routes.auth import register_auth_route
from routes.tasks import register_tasks_route
from routes.comments import register_comments_route
from db import init_db
import config

app = Flask(__name__)

register_auth_route(app)
register_users_route(app)
register_tasks_route(app)
register_comments_route(app)

@app.errorhandler(HTTPException)
def handle_http_exception(e):
			return jsonify({
				"error": e.description
			}), e.code

if __name__ == "__main__":
	init_db(config.DB_NAME)
	app.run(debug=True)