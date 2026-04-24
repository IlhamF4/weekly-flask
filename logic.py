import data

#return json of tasks
def get_tasks():
	return list(data.tasks.values())


#adding input from user to tasks
def add_task(title):
	new_task = {"id": data.current_id, "title": title, "done": False}
	data.tasks[data.current_id] = new_task
	data.current_id += 1
	return new_task


def update_task(task_id, title, done):
	task = data.tasks.get(task_id)
	
	if task is None:
		return None
	
	if title is not None:
		task["title"] = title
	if done is not None:
		task["done"] = done
		
	return task
	
def delete_task(task_id):
	task = data.tasks.get(task_id)
	
	if task is None:
		return None
		
	del data.tasks[task_id]
	
	return task
	