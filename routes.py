from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models import get_all_tasks, add_task, update_task, delete_task, delete_all_tasks, get_task_by_id

# Create a Blueprint for the routes
todo_bp = Blueprint('todo', __name__)

# Route to display tasks
@todo_bp.route('/', methods=['GET', 'POST'])
def todo_list():
    if request.method == 'POST':
        if 'task' in request.form:  # Add new task
            task = request.form['task']
            if task.strip():  # Ensure the task is not empty or just spaces
                add_task(task)
                return redirect(url_for('todo.todo_list'))
            else:
                return "Task cannot be empty", 400  # Return a 400 status code for empty tasks
        elif 'task_id' in request.form and 'new_task' in request.form:  # Update task
            task_id = request.form['task_id']
            new_task = request.form['new_task']
            update_task(task_id, new_task)
            return redirect(url_for('todo.todo_list'))

    tasks = get_all_tasks()
    
    # Check for JSON response request
    if request.headers.get("Accept") == "application/json" or request.args.get("format") == "json":
        return jsonify(tasks)  # Return tasks in JSON format

    return render_template('index.html', tasks=tasks)


# Route to delete a specific task
@todo_bp.route('/delete/<int:task_id>', methods=['GET'])
def delete_task_route(task_id):
    task = get_task_by_id(task_id)  # Fetch the task by ID
    if not task:
        return jsonify({"error": "Invalid task ID"}), 404  # Return JSON error for invalid ID
    delete_task(task_id)  # Delete the task
    return redirect(url_for('todo.todo_list'))  # Redirect to task list


# Route to delete all tasks
@todo_bp.route('/delete_all', methods=['GET'])
def delete_all_tasks_route():
    delete_all_tasks()
    
    # Handle JSON response request
    if request.headers.get("Accept") == "application/json" or request.args.get("format") == "json":
        return jsonify({"message": "All tasks deleted"})
    
    return redirect(url_for('todo.todo_list'))


# New API route for JSON task data
@todo_bp.route('/api/tasks', methods=['GET'])
def api_get_all_tasks():
    tasks = get_all_tasks()
    return jsonify(tasks)  # Always return tasks as JSON
