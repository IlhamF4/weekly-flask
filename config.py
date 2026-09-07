import os

DB_NAME = os.getenv("DB_NAME", "dev.db")
DB_URL = "postgresql://localhost:5432/task_manager"
