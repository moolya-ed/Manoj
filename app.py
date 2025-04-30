from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import Optional
from pydantic import BaseModel
import os
import json
import uuid

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static frontend (including styles)
frontend_path = os.path.join(os.path.dirname(__file__), "frontend")
app.mount("/frontend", StaticFiles(directory=frontend_path), name="static")

@app.get("/", response_class=HTMLResponse)
def read_root():
    return FileResponse(os.path.join(frontend_path, "index.html"))

# Pydantic model
class TodoCreate(BaseModel):
    title: str
    description: str
    doneStatus: Optional[bool] = False

# File path
DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "todos.json")

# Helpers
def load_list():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_list(todos):
    with open(DATA_FILE, "w") as f:
        json.dump(todos, f, indent=4)

def get_todo_details(todo_id):
    return next((todo for todo in load_list() if todo["id"] == todo_id), None)

def generate_id():
    return uuid.uuid4().hex

def add_todo(title, description, doneStatus=False):
    todos = load_list()
    new_todo = {
        "id": generate_id(),
        "title": title,
        "description": description,
        "doneStatus": doneStatus
    }
    todos.append(new_todo)
    save_list(todos)

def update_todo(todo_id, new_data):
    todos = load_list()
    for todo in todos:
        if todo["id"] == todo_id:
            todo.update(new_data)
            save_list(todos)
            return True
    return False

def remove_todo(todo_id):
    todos = load_list()
    new_list = [todo for todo in todos if todo["id"] != todo_id]
    if len(new_list) == len(todos):
        return False
    save_list(new_list)
    return True

# Routes
@app.get("/todos")
def get_all_todos(page: int = Query(1, ge=1), limit: int = Query(5, ge=1)):
    todos = load_list()
    start = (page - 1) * limit
    end = start + limit
    return {
        "page": page,
        "limit": limit,
        "total": len(todos),
        "todos": todos[start:end]
    }

@app.get("/todos/{todo_id}")
def get_todo(todo_id: str):
    todo = get_todo_details(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.post("/todos")
def create_todo(todo: TodoCreate):
    add_todo(todo.title, todo.description, todo.doneStatus)
    return {"message": "Todo created successfully"}

@app.put("/todos/{todo_id}")
def update_todo_route(
    todo_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    doneStatus: Optional[bool] = None,
):
    data = {}
    if title is not None: data["title"] = title
    if description is not None: data["description"] = description
    if doneStatus is not None: data["doneStatus"] = doneStatus

    if update_todo(todo_id, data):
        return {"message": "Todo updated successfully"}
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: str):
    if remove_todo(todo_id):
        return {"message": "Todo removed successfully"}
    raise HTTPException(status_code=404, detail="Todo not found")
