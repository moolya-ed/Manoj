import json
import os
import uuid


# Path to your JSON file
FILE_PATH = "data/todos.json"

FILE_PATH = os.path.join(os.path.dirname(__file__), "data", "todos.json")


# Load all todos from the JSON file
def load_list():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as file:

            return json.load(file)
    else:
        print("Todo file not found. Returning an empty list.")
        return []

# Save todos to the JSON file
def save_list(todo_list):
    with open(FILE_PATH, "w") as file:
        json.dump(todo_list, file, indent=4)

        todos = json.load(file)
        print(f"Loaded todos from file: {todos}")  # Debugging: Print loaded todos
        return todos
    else:
        print(f"{FILE_PATH} does not exist.")  # Debugging: If file is missing
        return []


# Save todos to the JSON file
def save_list(todo_list):
    try:
        with open(FILE_PATH, "w") as file:
            json.dump(todo_list, file, indent=4)
            print(f"Successfully saved to {FILE_PATH}")  # Debugging: Confirm save
    except Exception as e:
        print(f"Error saving to file: {e}")  # Debugging: Handle and report any errors

# Get details of a specific todo by ID
def get_todo_details(todo_id):
    todos = load_list()
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    return None  # Not found

# Remove a todo by ID
def remove_todo(todo_id):
    todos = load_list()
    new_todos = [todo for todo in todos if todo["id"] != todo_id]
    if len(todos) == len(new_todos):
        print("Todo ID not found.")
    else:
        save_list(new_todos)
        print("Todo removed successfully.")

# Update an existing todo by ID
def update_todo(todo_id, new_data):
    todos = load_list()
    updated = False
    for todo in todos:
        if todo["id"] == todo_id:
            todo.update(new_data)
            updated = True
            break
    if updated:
        save_list(todos)
        print("Todo updated successfully.")
    else:
        print("Todo ID not found.")

# Generate a unique ID
def generate_id():
    return uuid.uuid4().hex

    todos = load_list()  # Load the current list of todos
    print(f"Loaded todos: {todos}")  # Debugging: Print loaded todos

    updated = False
    for todo in todos:
        if todo["id"] == todo_id:
            print(f"Before Update: {todo}")  # Debugging: Print todo before updating
            todo.update(new_data)  # Update the todo item with new data
            print(f"After Update: {todo}")  # Debugging: Print todo after updating
            updated = True
            break

    if updated:
        print("Saving updated todo list.")  # Debugging: Indicate saving
        save_list(todos)  # Save the updated list back to the file
    else:
        print("Todo not found for update.")  # Debugging: If not found
    
    return updated

        
# Generate a unique ID
def generate_id():
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
        "id": generate_id()
    }
    todos.append(new_todo)
    save_list(todos)

print("New todo added successfully!")
print(load_list())
print(get_todo_details("8af52e54045b423aabaa9bcf7003ff4d"))
print(remove_todo("7f3d774efcad4dcbbccd891c2b121860"))
print(update_todo("8af52e54045b423aabaa9bcf7003ff4d", {"description": "Updated description", "doneStatus": True}))
print(generate_id())
print(add_todo("Learn Python", "Finish functions and loops section", False))


#print("New todo added successfully!")
#print(load_list())
#print(get_todo_details("8af52e54045b423aabaa9bcf7003ff4d"))
#print(remove_todo("7f3d774efcad4dcbbccd891c2b121860"))
#print(update_todo("8af52e54045b423aabaa9bcf7003ff4d", {"description": "Updated description", "doneStatus": True}))
#print(generate_id())
#print(add_todo("Learn Python", "Finish functions and loops section", False))                                             
