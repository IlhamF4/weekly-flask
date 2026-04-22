import data

#return json of tasks
def get_tasks():
	return data.tasks

#adding input from user to tasks
def add_task(title):
	new_task = {"id": data.current_id, "title":title, "done": False}
	data.tasks.append(new_task)
	data.current_id += 1
	return new_task

def update_task(task_id, title=None, done=None):
	task_index = find_task_index(task_id)
	if task_index is None:
		return None
		
	task = data.tasks[task_index]
	if title is not None:
		task["title"] = title
	if done is not None:
		task["done"] = done
	return task

def find_task_index(task_id):
	for i, task in enumerate(data.tasks):
		if task["id"] == task_id:
			return i
	return None
	
def delete_task(task_id):
	task_index = find_task_index(task_id)
	if task_index is None:
		return None
	del_task = data.tasks.pop(task_index)
	return del_task
	