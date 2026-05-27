Task Management API

Overview

A simple REST API for managing tasks with support for filtering, searching, sorting, and pagination.

---

Features

- Create, read, update, and delete tasks
- Filter by completion status ("done")
- Search tasks by title ("search")
- Sort tasks by ID ("sort")
- Pagination support ("page", "limit")

---

Setup

pip install -r requirements.txt


---

Run

gunicorn app:app --bind 0.0.0.0:8000

---

Environment Variable

DB_NAME
PORT

---

Endpoints

---

Tasks Domain

1. Create Task

POST /tasks

Request body:

{
  "title": "study"
}

---

2. Get Tasks

GET /tasks

Query parameters (optional):

- "done" → true / false
- "search" → string
- "sort" → asc / desc
- "page" → integer (default: 1)
- "limit" → integer (default: 10)

Examples:

/tasks
/tasks?done=true
/tasks?search=learn
/tasks?sort=desc
/tasks?page=2&limit=5
/tasks?done=true&search=study&sort=asc&page=1&limit=5

Response example:

{
  "data": [
    {
      "id": 1,
      "title": "study",
      "done": false
    }
  ],
  "meta": {
	"page": 1,
	"limit": 10,
	"count": 1
  }
}

---

3. Update Task

PUT /tasks/<id>

Request body:

{
  "title": "updated title",
  "done": true
}

---

4. Delete Task

DELETE /tasks/<id>

5. Archive Task

PATCH /tasks/<id>/archive

Comment cannot be created on archived task

6. Unarchive Task

PATCH /tasks/<id>/unarchive

---

Users Domain

(This domain is mostly deprecated and replaced by auth, this domain will change to admin operation gradually)

1. Create User

POST /users

Request body:

{
  "username": "admin"
}

2. Get Users

GET /users

Response example:

{
  "data": [
	{
		"user_id": 1, 
		"username": "admin"
	}
  ],
  "meta": {
	"page": 1,
	"limit": 10,
	"count": 1
  }
}


3. Update User

PUT /users

Request body:

{
  "username": "admin"
}

4. Delete User

DELETE /users

---

Auth Domain

1. Register User

POST /auth/register

Password is encrypted using bcrypt

Request body:

{
	"username": "admin", 
	"password": "abcd1234"
}

2. Login User

POST /auth/Login

Request body:

{
	"username": "admin", 
	"password": "abcd1234"
}

---

Comments Domain

1. Create Comment

POST /tasks/<id>/comments

Request body:

{
	"content": "test comment"
}

2. Get Comment

GET /tasks/<id>/comments

Response examples:

{
  "data": [
	{
		"comment_id": 1, 
		"task_id": 1, 
		"user_id": 1, 
		"content": "test comment", 
		"created_at": 2026-05-31
	}
  ],
  "meta": {
	"page": 1,
	"limit": 10,
	"count": 1
  }
}

3. Delete Comment

DELETE /comments/<comment_id>

using soft delete flag

4. Restore Comment

PATCH /comments/<comment_id>

Restore comment is idempotent
---

Notes

- All inputs are validated
- Invalid input will return a "400 Bad Request"
- If an action is unauthorized a "403 Forbidden" is returned
- If a resource is not found, a "404 Not Found" is returned
- If a resource already exist, a "409 Conflict" is returned

Test is inside folder "test/", it test logic function using pytest

All endpoint or user interface is inside "route/" folder, while domain and business logic is inside "logic/" folder.

There is 2 database, task.db for production, while test.db for test.

db.py contain infrastructure code (database config)

Database: prod.db (for production), dev.db (for development), test.db (for testing)