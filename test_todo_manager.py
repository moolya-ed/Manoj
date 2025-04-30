import unittest
from unittest.mock import patch
from todo_manager import add_todo, load_list, save_list, generate_id  # Import from todo_manager.py

class TestAddTodo(unittest.TestCase):
    
    @patch('todo_manager.load_list')  # Mocking load_list function
    @patch('todo_manager.save_list')  # Mocking save_list function
    @patch('todo_manager.generate_id')  # Mocking generate_id function
    def test_add_todo(self, mock_generate_id, mock_save_list, mock_load_list):
        # Mocking load_list to return an empty list (no todos yet)
        mock_load_list.return_value = []

        # Mocking generate_id to return a fixed value
        mock_generate_id.return_value = "mocked-id-1234"

        # Mocking save_list so it doesn't write to the file system
        mock_save_list.return_value = None  # Just to ensure no actual file operation occurs

        # Sample data for creating a new todo
        title = "Test Todo"
        description = "This is a test description"
        doneStatus = False

        # Call the function we're testing
        add_todo(title, description, doneStatus)

        # Assert that load_list() was called to load the existing todos
        mock_load_list.assert_called_once()

        # Assert that generate_id() was called once to generate a new unique ID
        mock_generate_id.assert_called_once()

        # Assert that save_list() was called once with the new todo
        mock_save_list.assert_called_once_with([{
            "title": title,
            "description": description,
            "doneStatus": doneStatus,
            "id": "mocked-id-1234"
        }])

if __name__ == '__main__':
    unittest.main()
