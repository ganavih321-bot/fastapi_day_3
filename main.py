from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Simple In-Memory Todo API",
    description="A simple FastAPI Todo application storing items in an in-memory dictionary.",
    version="1.0.0",
)

# In-memory dictionary storage and ID counter
todos_db: Dict[int, dict] = {}
current_id: int = 1


# Pydantic Schemas
class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, example="Buy groceries")
    description: Optional[str] = Field(None, example="Milk, bread, and eggs")
    completed: bool = Field(default=False, example=False)


class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, example="Buy groceries and snacks")
    description: Optional[str] = Field(None, example="Milk, bread, eggs, and fruits")
    completed: Optional[bool] = Field(None, example=True)


class TodoItem(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool


@app.get("/", tags=["General"])
async def root():
    return {
        "message": "Welcome to the Simple Todo API!",
        "docs_url": "/docs",
        "todos_url": "/todos",
    }


@app.get("/todos", response_model=List[TodoItem], tags=["Todos"])
async def get_todos(
    completed: Optional[bool] = Query(
        None, description="Filter todos by completed status"
    )
):
    """Retrieve all todo items with optional filter by completion status."""
    if completed is not None:
        return [todo for todo in todos_db.values() if todo["completed"] == completed]
    return list(todos_db.values())


@app.get("/todos/{todo_id}", response_model=TodoItem, tags=["Todos"])
async def get_todo(todo_id: int):
    """Retrieve a specific todo item by its ID."""
    if todo_id not in todos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo item with ID {todo_id} not found",
        )
    return todos_db[todo_id]


@app.post(
    "/todos",
    response_model=TodoItem,
    status_code=status.HTTP_201_CREATED,
    tags=["Todos"],
)
async def create_todo(todo: TodoCreate):
    """Create a new todo item and store it in the in-memory dictionary."""
    global current_id
    new_todo = {
        "id": current_id,
        "title": todo.title,
        "description": todo.description,
        "completed": todo.completed,
    }
    todos_db[current_id] = new_todo
    current_id += 1
    return new_todo


@app.put("/todos/{todo_id}", response_model=TodoItem, tags=["Todos"])
async def update_todo(todo_id: int, todo_update: TodoUpdate):
    """Update an existing todo item."""
    if todo_id not in todos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo item with ID {todo_id} not found",
        )

    stored_todo = todos_db[todo_id]
    update_data = todo_update.model_dump(exclude_unset=True)

    stored_todo.update(update_data)
    todos_db[todo_id] = stored_todo
    return stored_todo


@app.delete(
    "/todos/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Todos"],
)
async def delete_todo(todo_id: int):
    """Delete a todo item from the in-memory dictionary."""
    if todo_id not in todos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo item with ID {todo_id} not found",
        )
    del todos_db[todo_id]
    return None