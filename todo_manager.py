import json
import os
import logging

# Load the list of todos
def load_list():
    file_path = "data/todos.json"

    if not os.path.exists(file_path):
        logging.warning("Todo file not found. Returning empty list.")
        return []

    try:
        with open(file_path, 'r') as file:
            todos = json.load(file)
            return todos
    except Exception as e:
        logging.error(f"Error reading the todo file: {e}")
        return []

# Get details of a specific todo
def get_todo_details(todo_id):
    todos = load_list()
    for todo in todos:
        if todo.get("id") == todo_id:
            return todo
    raise Exception(f"404 Not Found: Todo with ID {todo_id} not found.")

# Example usage
if __name__ == "__main__":
    # Load all todos
    all_todos = load_list()
    print("All Todos:")
    for t in all_todos:
        print(f"- {t['title']} (ID: {t['id']})")

    # Try to get a todo by ID
    print("\nGetting details of one Todo:")
    try:
        todo = get_todo_details("8af52e54045b423aabaa9bcf7003ff4d")  # You can change this ID
        print(todo)
    except Exception as e:
        print(e)
