import unittest
from app import app  # Import your Flask app
from models import get_db_connection  # Import your DB connection function

class TodoAppTestCase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Set up the test database."""
        cls.conn = get_db_connection()
        cur = cls.conn.cursor()
        cur.execute("DELETE FROM tasks")  # Clean the tasks table before tests
        cls.conn.commit()
        cur.close()

    @classmethod
    def tearDownClass(cls):
        """Tear down the test database."""
        cls.conn.close()

    def setUp(self):
        """Set up the test client for each test."""
        self.client = app.test_client()
        self.client.testing = True

    def test_get_todo_list(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Todo List", response.data)

    def test_add_task(self):
        response = self.client.post('/', data={'task': 'Test Task'})
        self.assertEqual(response.status_code, 302)
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM tasks WHERE task = %s", ('Test Task',))
        task = cur.fetchone()
        cur.close()
        self.assertIsNotNone(task)

    def test_update_task(self):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO tasks (task) VALUES (%s) RETURNING id", ('Old Task',))
        task_id = cur.fetchone()[0]
        self.conn.commit()
        cur.close()

        response = self.client.post('/', data={'task_id': task_id, 'new_task': 'Updated Task'})
        self.assertEqual(response.status_code, 302)
        cur = self.conn.cursor()
        cur.execute("SELECT task FROM tasks WHERE id = %s", (task_id,))
        task = cur.fetchone()
        cur.close()
        self.assertEqual(task[0], 'Updated Task')

    def test_delete_task(self):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO tasks (task) VALUES (%s) RETURNING id", ('Task to Delete',))
        task_id = cur.fetchone()[0]
        self.conn.commit()
        cur.close()

        response = self.client.get(f'/delete/{task_id}')
        self.assertEqual(response.status_code, 302)
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
        task = cur.fetchone()
        cur.close()
        self.assertIsNone(task)

    def test_delete_all(self):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO tasks (task) VALUES (%s)", ('Task 1',))
        cur.execute("INSERT INTO tasks (task) VALUES (%s)", ('Task 2',))
        self.conn.commit()
        cur.close()

        response = self.client.get('/delete_all')
        self.assertEqual(response.status_code, 302)
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM tasks")
        tasks = cur.fetchall()
        cur.close()
        self.assertEqual(len(tasks), 0)
        
        

    def test_delete_all_when_empty(self):
        """Test deleting all tasks when the tasks table is empty."""
        cur = self.conn.cursor()
        cur.execute("DELETE FROM tasks")  # Clean the tasks table before testing
        self.conn.commit()
        cur.close()

        response = self.client.get('/delete_all')
        self.assertEqual(response.status_code, 302)  # Should redirect after attempting to delete all tasks

        cur = self.conn.cursor()
        cur.execute("SELECT * FROM tasks")
        tasks = cur.fetchall()
        cur.close()
        self.assertEqual(len(tasks), 0)  # Ensure the table is still empty
        
        

    def test_add_empty_task(self):
        """Test that an empty task cannot be added."""
        # Attempt to add an empty task
        response = self.client.post('/', data={'task': ''})
        
        # Check if the response status code is 400 (Bad Request) for invalid input
        self.assertEqual(response.status_code, 400)
        
        # Verify that no new task is added to the database
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM tasks WHERE task = ''")
        task = cur.fetchone()
        cur.close()
        
        # Ensure no empty task exists in the database
        self.assertIsNone(task)

    def test_delete_invalid_task(self):
    
        invalid_task_id = 9999  # This ID should not exist in the DB

    # Make the DELETE request
        response = self.client.get(f'/delete/{invalid_task_id}')
    
    # Assert that the status code is 404 (Not Found)
        self.assertEqual(response.status_code, 404)
    
    def test_update_invalid_task(self):
    
        invalid_task_id = 9990  # This ID should not exist in the DB

    # Make the update request
        response = self.client.put(f'/update/{invalid_task_id}')
    
    # Assert that the status code is 404 (Not Found)
        self.assertEqual(response.status_code, 404)
        
    def test_delete_already_deleted_task(self):
    # Insert a task into the database
        cur = self.conn.cursor()
        cur.execute("INSERT INTO tasks (task) VALUES (%s) RETURNING id", ('Task to Delete Twice',))
        task_id = cur.fetchone()[0]
        self.conn.commit()
        cur.close()

        # Delete the task
        response = self.client.get(f'/delete/{task_id}')
        self.assertEqual(response.status_code, 302)  # Ensure the first delete was successful

        # Attempt to delete the same task again
        response = self.client.get(f'/delete/{task_id}')
        self.assertEqual(response.status_code, 404)  # Task should no longer exist