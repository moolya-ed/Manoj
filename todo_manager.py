import json
import os
import logging
import uuid

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
        logging.error(f"Errorsreading the todo file: {e}")
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
        
        todo = get_todo_details("8af52e54045b423aabaa9bcf7003ff4d")
# You can change this ID
        print(todo)
    except Exception as e:
        print(e)


def save_list(todo_list):
    file_path = "data/todos.json"

    try:
        with open(file_path, 'w') as file:
            json.dump(todo_list, file, indent=4)
            logging.info("Todos saved successfully.")
    except Exception as e:
        logging.error(f"Error saving the todo list: {e}")


def remove_todo(todo_id):
    todos = load_list()
    original_length = len(todos)

    # Filter out the todo with the matching ID
    updated_todos = [todo for todo in todos if todo.get("id") != todo_id]

    if len(updated_todos) == original_length:
        # No item was removed, which means the ID was not found
        raise Exception(f"404 Not Found: Todo with ID {todo_id} not found.")

    # Save the updated list
    save_list(updated_todos)
    logging.info(f"Todo with ID {todo_id} removed successfully.")


def update_todo(todo_id, todo):
    todos = load_list()
    todo_found = False

    for t in todos:
        if t.get("id") == todo_id:
            t.update(todo)  # Only update fields provided in the input
            todo_found = True
            break

    if not todo_found:
        raise Exception(f"404 Not Found: Todo with ID {todo_id} not found.")

    save_list(todos)
    logging.info(f"Todo with ID {todo_id} updated successfully.")



def generate_id():
    return uuid.uuid4().hex

def add_todo(title, description, done_status=False):
    todos = load_list()
    new_todo = {
        "title": title,
        "description": description,
        "doneStatus": done_status,
        "id": generate_id()
    }
    todos.append(new_todo)
    save_list(todos)
    print("New todo added successfully!")




