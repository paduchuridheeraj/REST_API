# Robot Management REST API

This backend is built to manage robots and their activity. It provides APIs to register robots, update their status, view robot details, and store or retrieve activity logs.

## Features

- Register a new robot with id, name, type, and status
- Update robot status: battery percent, location, mode, error state
- Get a list of all robots
- Get details of a specific robot
- Create logs for robot activity or errors
- View all logs for a specific robot
- Uses SQLite database via SQLAlchemy
- Auto-generated Swagger UI with FastAPI

## Tech Stack

- Python
- FastAPI
- Uvicorn
- SQLite
- SQLAlchemy

## Setup

### 1. Create and activate virtual environment

```bash
python -m venv venv

#### 2. Install dependencies
pip install -r requirements.txt

#### 3. Run the server
uvicorn app.main:app --reload
