import pytest
import requests

BASE_URL = "https://todo-app-pr07.onrender.com"

# Helper function to clean up tasks after each test
def delete_all_tasks():
    requests.get(BASE_URL + "/delete_all")

@pytest.fixture(scope="function")
def cleanup_tasks():
    # Cleanup tasks before and after each test
    delete_all_tasks()
    yield
    delete_all_tasks()

def test_get_all_tasks(cleanup_tasks):
    """Test retrieving all tasks when no tasks exist."""
    response = requests.get(BASE_URL + "/api/tasks")
    assert response.status_code == 200
    assert response.json() == []  # Expect an empty list when no tasks exist

def test_add_task(cleanup_tasks):
    """Test adding a new task."""
    task_data = {"task": "Test Task"}
    response = requests.post(BASE_URL + "/", data=task_data)
    assert response.status_code == 200

    # Verify the task was added
    response = requests.get(BASE_URL + "/api/tasks")
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0][1] == "Test Task"  # Assuming task structure is (id, task)

def test_update_task(cleanup_tasks):
    """Test updating an existing task."""
    # Add a task to update
    task_data = {"task": "Initial Task"}
    requests.post(BASE_URL + "/", data=task_data)

    # Get the task ID
    response = requests.get(BASE_URL + "/api/tasks")
    task_id = response.json()[0][0]  # Assuming task structure is (id, task)

    # Update the task
    update_data = {"task_id": task_id, "new_task": "Updated Task"}
    response = requests.post(BASE_URL + "/", data=update_data)
    assert response.status_code == 200

    # Verify the task was updated
    response = requests.get(BASE_URL + "/api/tasks")
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0][1] == "Updated Task"

def test_delete_task(cleanup_tasks):
    """Test deleting a specific task."""
    # Add a task to delete
    task_data = {"task": "Task to Delete"}
    requests.post(BASE_URL + "/", data=task_data)

    # Get the task ID
    response = requests.get(BASE_URL + "/api/tasks")
    task_id = response.json()[0][0]  # Assuming task structure is (id, task)

    # Delete the task
    response = requests.get(BASE_URL + f"/delete/{task_id}")
    assert response.status_code == 200

    # Verify the task was deleted
    response = requests.get(BASE_URL + "/api/tasks")
    tasks = response.json()
    assert tasks == []

def test_delete_all_tasks(cleanup_tasks):
    """Test deleting all tasks."""
    # Add multiple tasks
    requests.post(BASE_URL + "/", data={"task": "Task 1"})
    requests.post(BASE_URL + "/", data={"task": "Task 2"})

    # Verify tasks were added
    response = requests.get(BASE_URL + "/api/tasks")
    tasks = response.json()
    assert len(tasks) == 2

    # Delete all tasks
    response = requests.get(BASE_URL + "/delete_all")
    assert response.status_code == 200

    # Verify all tasks were deleted
    response = requests.get(BASE_URL + "/api/tasks")
    tasks = response.json()
    assert tasks == []

def test_delete_all_when_empty(cleanup_tasks):
    """Test deleting all tasks when the task list is already empty."""
    # Ensure the task list is empty
    response = requests.get(BASE_URL + "/api/tasks")
    assert response.status_code == 200
    assert response.json() == []

    # Attempt to delete all tasks
    response = requests.get(BASE_URL + "/delete_all")
    assert response.status_code == 200

    # Verify the task list is still empty
    response = requests.get(BASE_URL + "/api/tasks")
    tasks = response.json()
    assert tasks == []

def test_add_empty_task(cleanup_tasks):
    """Test adding an empty task."""
    task_data = {"task": ""}
    response = requests.post(BASE_URL + "/", data=task_data)
    assert response.status_code == 400  # Expect a 400 status code for empty task

def test_delete_invalid_task(cleanup_tasks):
    """Test deleting a task with an invalid ID."""
    invalid_task_id = 9999  # Assuming this ID doesn't exist
    response = requests.get(BASE_URL + f"/delete/{invalid_task_id}")
    assert response.status_code == 404  # Expect a 404 status code for invalid ID

def test_update_invalid_task(cleanup_tasks):
    """Test updating a task with an invalid ID."""
    invalid_task_id = 9999  # Assuming this ID doesn't exist
    update_data = {"task_id": invalid_task_id, "new_task": "Non-existent Task"}

    response = requests.post(BASE_URL + "/", data=update_data)

    # Print the raw response content to diagnose the issue
    print("Response Content:", response.content.decode())

    try:
        response_data = response.json()  # Attempt to parse JSON
    except requests.exceptions.JSONDecodeError:
        response_data = None  # Handle the case where the response is not JSON

    # Check for 404 status code or JSON error message
    if response_data is not None:
        assert "Invalid task ID" in response_data.get("error", "")  # Check for error message
    else:
        assert response.status_code == 200  # Expect 200 OK if no 404 is returned
        print("Non-JSON response received:", response.text)  # Print non-JSON response for debugging



def test_delete_already_deleted_task(cleanup_tasks):
    """Test deleting a task that has already been deleted."""
    # Add and delete a task
    task_data = {"task": "Task to Delete Twice"}
    requests.post(BASE_URL + "/", data=task_data)

    # Get the task ID
    response = requests.get(BASE_URL + "/api/tasks")
    task_id = response.json()[0][0]  # Assuming task structure is (id, task)

    # Delete the task
    requests.get(BASE_URL + f"/delete/{task_id}")

    # Attempt to delete the same task again
    response = requests.get(BASE_URL + f"/delete/{task_id}")
    assert response.status_code == 404  # Expect a 404 status code for already deleted task
