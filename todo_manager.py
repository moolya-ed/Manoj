import json
import os
import uuid
import logging

# Path to your JSON file
FILE_PATH = "data/todos.json"
FILE_PATH = os.path.join(os.path.dirname(__file__), "data", "todos.json")

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("app.log")]
)

# Load all todos from the JSON file
def load_list():
    if os.path.exists(FILE_PATH):
        try:
            with open(FILE_PATH, "r") as file:
                todos = json.load(file)
                logging.info("Successfully loaded todos from file.")
                return todos
        except Exception as e:
            logging.error(f"Error loading todos: {e}")
            return []
    else:
        logging.warning("Todo file not found. Returning an empty list.")
        return []

# Save todos to the JSON file
def save_list(todo_list):
    try:
        with open(FILE_PATH, "w") as file:
            json.dump(todo_list, file, indent=4)
            logging.info(f"Successfully saved todos to {FILE_PATH}")
    except Exception as e:
        logging.error(f"Error saving todos to file: {e}")

# Get details of a specific todo by ID
def get_todo_details(todo_id):
    todos = load_list()
    for todo in todos:
        if todo["id"] == todo_id:
            logging.info(f"Found todo with ID {todo_id}.")
            return todo
    logging.warning(f"Todo with ID {todo_id} not found.")
    return None  # Not found

# Remove a todo by ID
def remove_todo(todo_id):
    todos = load_list()
    new_todos = [todo for todo in todos if todo["id"] != todo_id]
    if len(todos) == len(new_todos):
        logging.warning(f"Todo ID {todo_id} not found.")
    else:
        save_list(new_todos)
        logging.info(f"Todo with ID {todo_id} removed successfully.")

# Update an existing todo by ID
def update_todo(todo_id, new_data):
    todos = load_list()
    updated = False
    for todo in todos:
        if todo["id"] == todo_id:
            todo.update(new_data)
            updated = True
            logging.info(f"Todo with ID {todo_id} updated successfully.")
            break
    if updated:
        save_list(todos)
    else:
        logging.warning(f"Todo ID {todo_id} not found.")

# Generate a unique ID
def generate_id():
    return uuid.uuid4().hex

# Generate a numeric ID based on the current highest ID
def generate_numeric_id():
    todos = load_list()
    if not todos:
        return "1"
    return str(int(max(todo["id"] for todo in todos)) + 1)

# Add a new todo
def add_todo(title, description, doneStatus=False):
    todos = load_list()
    new_todo = {
        "title": title,
        "description": description,
        "doneStatus": doneStatus,
        "id": generate_id()  # Uses UUID to generate unique ID
    }
    todos.append(new_todo)
    save_list(todos)
    logging.info(f"New todo added: {new_todo}")

# Test the functions
logging.info("Starting todo operations...")

# Example operations
add_todo("Learn Python", "Finish functions and loops section", False)
logging.info(f"All Todos: {load_list()}")
logging.info(f"Todo Details: {get_todo_details('8af52e54045b423aabaa9bcf7003ff4d')}")
remove_todo("7f3d774efcad4dcbbccd891c2b121860")
update_todo("8af52e54045b423aabaa9bcf7003ff4d", {"description": "Updated description", "doneStatus": True})

logging.info(f"Generated ID: {generate_id()}")
