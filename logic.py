from data import tasks

#return json of tasks
def get_tasks():
	return tasks

#adding input from user to tasks
def add_task(title):
	tasks.append(title)
	return {"message": "added", "task": title}