const apiUrl = "http://127.0.0.1:8080/todos";

async function fetchTodos() {
    const response = await fetch(apiUrl);
    const todos = await response.json();
    const todoList = document.getElementById("todo-list");
    todoList.innerHTML = '';

    todos.forEach(todo => {
        const li = document.createElement("li");
        li.textContent = `${todo.title} - ${todo.doneStatus ? "Done" : "Not Done"}`;
        todoList.appendChild(li);
    });
}

async function createTodo(event) {
    event.preventDefault();
    const title = document.getElementById("title").value;
    const description = document.getElementById("description").value;
    const doneStatus = document.getElementById("doneStatus").checked;

    const response = await fetch(apiUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ title, description, doneStatus })
    });

    const message = document.getElementById("message");
    if (response.ok) {
        message.textContent = "Todo created successfully!";
        fetchTodos(); // Optional: refresh list
    } else {
        message.textContent = "Failed to create Todo.";
    }
}

async function updateTodo(event) {
    event.preventDefault();
    const todoId = document.getElementById("todo-id").value.trim();
    const title = document.getElementById("title").value.trim();
    const description = document.getElementById("description").value.trim();
    const doneStatus = document.getElementById("doneStatus").checked;

    const queryParams = [];
    if (title !== '') queryParams.push(`title=${encodeURIComponent(title)}`);
    if (description !== '') queryParams.push(`description=${encodeURIComponent(description)}`);
    queryParams.push(`doneStatus=${doneStatus}`);

    const queryString = queryParams.length ? `?${queryParams.join('&')}` : '';

    const response = await fetch(`${apiUrl}/${todoId}${queryString}`, {
        method: "PUT"
    });

    const message = document.getElementById("message");
    if (response.ok) {
        message.textContent = "Todo updated successfully!";
        fetchTodos(); // Optional: refresh list
    } else {
        message.textContent = "Failed to update Todo.";
    }
}

async function deleteTodo(event) {
    event.preventDefault();
    const todoId = document.getElementById("todo-id").value.trim();

    const response = await fetch(`${apiUrl}/${todoId}`, {
        method: "DELETE"
    });

    const message = document.getElementById("message");
    if (response.ok) {
        message.textContent = "Todo deleted successfully!";
        fetchTodos(); // Optional: refresh list
    } else {
        message.textContent = "Failed to delete Todo.";
    }
}

// Bind forms to their handlers
if (document.getElementById("create-todo-form")) {
    document.getElementById("create-todo-form").addEventListener("submit", createTodo);
}

if (document.getElementById("update-todo-form")) {
    document.getElementById("update-todo-form").addEventListener("submit", updateTodo);
}

if (document.getElementById("delete-todo-form")) {
    document.getElementById("delete-todo-form").addEventListener("submit", deleteTodo);
}

// Fetch todos on page load if the list element exists
if (document.getElementById("todo-list")) {
    fetchTodos();
}
