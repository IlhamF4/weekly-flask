from flask import Flask, jsonify
from werkzeug.exceptions import BadRequest, NotFound, HTTPException, Forbidden
from routes.users import register_users_route
from routes.auth import register_auth_route
from routes.tasks import register_tasks_route
from routes.comments import register_comments_route
from db import init_db
import config
import logging

logging.basicConfig(encoding="utf-8", level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

logger = logging.getLogger(__name__)
logger.info(f"Application started with database {config.DB_NAME}")

init_db(config.DB_NAME)

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


@app.errorhandler(Exception)
def handle_error(e):
	logger.exception("Unexpected error")
	return jsonify({
		"500 Internal server error"
	}), 500


#if __name__ == "__main__":
#	init_db(config.DB_NAME)
#	port = int(os.getenv("PORT", 5000))
#	app.run(host="0.0.0.0", port=port)