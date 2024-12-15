from flask import Blueprint, render_template, request, redirect, url_for
from models import get_all_tasks, add_task, update_task, delete_task, delete_all_tasks, get_task_by_id

todo_bp = Blueprint('todo', __name__)

# Add task (POST method)
@todo_bp.route('/', methods=['POST'])
def add_task_route():
    task = request.form['task']
    if task.strip():
        add_task(task)
        return '', 201  # Return status 201 for created task
    return "Task cannot be empty", 400

# Get all tasks (GET method)
@todo_bp.route('/', methods=['GET'])
def get_tasks():
    tasks = get_all_tasks()
    return {'tasks': tasks}, 200

# Update task (POST method)
@todo_bp.route('/', methods=['POST'])
def update_task_route():
    task_id = request.form['task_id']
    new_task = request.form['new_task']
    update_task(task_id, new_task)
    return '', 200  # Status 200 for successful update

# Delete a task (DELETE method)
@todo_bp.route('/delete/<int:task_id>', methods=['DELETE'])
def delete_task_route(task_id):
    task = get_task_by_id(task_id)
    if not task:
        return "Invalid task ID", 404
    delete_task(task_id)
    return '', 204  # Status 204 for no content (successful delete)

# Delete all tasks (DELETE method)
@todo_bp.route('/delete_all', methods=['DELETE'])
def delete_all_tasks_route():
    delete_all_tasks()
    return '', 204  # Status 204 for successful delete all
