# Todo App

A simple **To-Do Application** built using **Flask** and **PostgreSQL** for managing tasks. This application allows users to add, update, delete, and view tasks via both a web interface and a RESTful API. It is designed to be easy to set up and use.

![image](https://github.com/user-attachments/assets/11562daa-38e7-44c3-aecb-b0d3c899b3d3)


---

## Features-

- **Add a New To-Do Task**: Users can create new tasks.
- **Display List of To-Do Tasks**: View all tasks currently stored in the database.
- **Edit/Update a To-Do Task**: Modify specific tasks by their unique ID.
- **Delete a Specific To-Do Task**: Remove individual tasks by their unique ID.
- **Delete All To-Do Tasks**: Clear the entire task list in one action.

---

## Tech Stack-

- **Backend**: Python (Flask)
- **Database**: PostgreSQL
- **Deployment**:Render Platform

---

## Setup Instructions-

1.Clone the repository to your local machine using the following command:

```bash
git clone https://github.com/yourusername/todo_app.git
```

2.Navigate to the Project Directory
```bash
cd todo_app
```

3.Create a Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

4.Install Dependencies
```bash
pip install -r requirements.txt
```
5.Set Up PostgreSQL  
Ensure you have PostgreSQL installed and running.  
Create a new PostgreSQL database for the application. 

6.Run the app locally:
```bash
python app.py
```
The application will be accessible at http://127.0.0.1:5000  

---

## API Endpoints-  

-**GET /tasks**: Retrieve the list of all tasks.
- **POST /tasks**: Create a new task.
- **GET /tasks/{id}**: Retrieve a specific task by its ID.
- **PUT /tasks/{id}**: Update a specific task by its ID.
- **DELETE /tasks/{id}**: Delete a specific task by its ID.
- **DELETE /tasks**: Delete all tasks.

## Deployment-
The application is deployed and accessible at the following URL:

[https://todo-app-pr07.onrender.com/](https://todo-app-pr07.onrender.com/)

**Note**: Loading the app on the hosted service may take some time as we are using the free plan on Render.

## Testing-

To run the tests for this application, follow these steps:

1. **Install Testing Dependencies**  
   If you haven't already, install the required dependencies for testing.
   ```bash
   pip install pytest requests
   ```
## Running Tests with pytest-
1. Make sure to install the required dependencies mentioned above.  
2. Save your test file as `test_app.py` on your local machine.  
3. Open a terminal or command prompt, navigate to the location of the `test_app.py` file, and run the following command:
 ```bash
 pytest test_app.py
 ```
4. After running the command, pytest will execute the test cases in test_app.py. Based on the test cases passed, you will see an output indicating the number of tests that passed. For example:
```bash
 10 passed
```
![5d8aa84f-0e46-4495-876f-fc97b9c58002](https://github.com/user-attachments/assets/03b2cfb2-92b2-46b0-b51d-990262fee308)

## Test Cases made for this To-Do Application-
- **Test retrieving all tasks when no tasks exist**
- **Test adding a new task**
- **Test updating an existing task**
- **Test deleting a specific task**
- **Test deleting all tasks**
- **Test deleting all tasks when the task list is empty**
- **Test adding an empty task**
- **Test deleting a task with an invalid ID**
- **Test updating a task with an invalid ID**
- **Test deleting a task that has already been deleted**







