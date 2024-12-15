from flask import Blueprint, render_template, request, redirect, url_for
from models import get_all_tasks, add_task, update_task, delete_task, delete_all_tasks
from models import get_task_by_id  # Add this import statement


# Create a Blueprint for the routes
todo_bp = Blueprint('todo', _name_)

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
                # Handle the case where the task is empty
                return "Task cannot be empty", 400  # Return a 400 status code for empty tasks
        elif 'task_id' in request.form and 'new_task' in request.form:  # Update task
            task_id = request.form['task_id']
            new_task = request.form['new_task']
            update_task(task_id, new_task)
            return redirect(url_for('todo.todo_list'))

    tasks = get_all_tasks()
    return render_template('index.html', tasks=tasks)



### Route to delete a specific task
#@todo_bp.route('/delete/<int:task_id>', methods=['GET'])
##def delete_task_route(task_id):
  ##  delete_task(task_id)
    ##return redirect(url_for('todo.todo_list'))


@todo_bp.route('/delete/<int:task_id>', methods=['GET'])
def delete_task_route(task_id):
    task = get_task_by_id(task_id)  # Now it will correctly reference the function
    
    if not task:
        return "Invalid task ID", 404  # If task doesn't exist, return 404
    
    delete_task(task_id)  # Delete the task if it exists
    return redirect(url_for('todo.todo_list'))  # Redirect after deletion


# Route to delete all tasks
@todo_bp.route('/delete_all', methods=['GET'])
def delete_all_tasks_route():
    delete_all_tasks()
    return redirect(url_for('todo.todo_list'))
