
from fastapi import FastAPI

# Create FastAPI application
app = FastAPI(
    title="Basic FastAPI Application",
    description="My first FastAPI application for Social Eagle Assignment 4",
    version="1.0.0"
)


# Endpoint 1: Root endpoint
@app.get("/")
def home():
    return {
        "message": "Hello, FastAPI!",
        "status": "Application is running successfully"
    }


# Endpoint 2: Greeting endpoint with path parameter
@app.get("/greet/{name}")
def greet_user(name: str):
    return {
        "message": f"Hello, {name}! Welcome to FastAPI.",
        "name": name
    }
