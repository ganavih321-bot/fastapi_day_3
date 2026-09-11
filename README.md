# FastAPI In-Memory Todo App

A simple RESTful Todo API built using **FastAPI** that stores items in an in-memory dictionary (no database required).

## Features

- **Full CRUD operations**:
  - `GET /todos` - List all todos (with optional `?completed=true|false` filter)
  - `GET /todos/{id}` - Get a single todo by ID
  - `POST /todos` - Create a new todo item
  - `PUT /todos/{id}` - Update a todo item
  - `DELETE /todos/{id}` - Delete a todo item
- **Data validation** using Pydantic schemas.
- **Interactive API Documentation** powered by Swagger UI and ReDoc.

## Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Server

```bash
uvicorn main:app --reload
```

The server will start at `http://127.0.0.1:8000`.

### 3. Interactive API Documentation

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
