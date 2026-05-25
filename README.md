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

pip install flask
python app.py

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
  "tasks": [
    {
      "id": 1,
      "title": "study",
      "done": false
    }
  ]
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

1. Create User

POST /users

Request body:

{
  "username": "admin"
}

2. Get Users

GET /users

Response example:

{"data": {


3. Update User

PUT /users

Request body:

{
  "username": "admin"
}

4. Delete User

DELETE /users

---

Notes

- All inputs are validated
- Invalid input will return a "400 Bad Request"
- If a task is not found, a "404 Not Found" is returned