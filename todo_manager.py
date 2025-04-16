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
        todo = get_todo_details("")  # You can change this ID
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

import uuid

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

def menu():
    while True:
        print("\nTodo Management Menu:")
        print("1. View All Todos")
        print("2. Get Todo Details")
        print("3. Add a todo")
        print("4. Remove a Todo")
        print("5. Update a Todo")
        print("6. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            todos = load_list()
            print("\nAll Todos:")
            for t in todos:
                print(f"- {t['title']} (ID: {t['id']})")

        elif choice == "2":
            todo_id = input("Enter Todo ID: ")
            try:
                todo = get_todo_details(todo_id)
                print(f"\nDetails of Todo ID {todo_id}:")
                print(todo)
            except Exception as e:
                print(e)
        elif choice == "3":
            title = input("Title: ")
            desc = input("Description: ")
            status_input = input("Done? (true/false): ").lower()
            status = status_input == "true"
            add_todo(title, desc, status)     

        elif choice == "4":
            todo_id = input("Enter Todo ID to remove: ")
            try:
                remove_todo(todo_id)
                print("Todo removed successfully.")
            except Exception as e:
                print(e)

        elif choice == "5":
            todo_id = input("Enter Todo ID to update: ")
            print("Enter new values (leave blank to skip):")
            title = input("Title: ")
            description = input("Description: ")
            done_status_input = input("Done? (true/false): ")

            todo = {}
            if title:
                todo["title"] = title
            if description:
                todo["description"] = description
            if done_status_input.lower() in ["true", "false"]:
                todo["doneStatus"] = done_status_input.lower() == "true"

            try:
                update_todo(todo_id, todo)
                print("Todo updated successfully.")
            except Exception as e:
                print(e)

        elif choice == "6":
            print("Exiting... 👋")
            break
        else:
            print("Invalid choice. Please try again.")

# -----------------------------
# Entry Point
# -----------------------------
if __name__ == "__main__":
    menu()






