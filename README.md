# TaskFlow API



A simple Django REST Framework project for managing personal tasks.
It supports CRUD operations, user authentication with JWT, and ensures that tasks belong to their owners.

## Features

User registration & authentication (JWT with SimpleJWT)

Create, Read, Update, and Delete tasks

Each task is tied to its owner

Secure endpoints (only authenticated users can interact)

Pagination & query parameters for listing tasks
 Throttling via **DRF’s throttling system** to prevent abuse

## Tech Stack

Python 3.13+

Django 5

Django REST Framework (DRF)

djangorestframework-simplejwt

## Installation & Setup
### 1. Clone the repo
```bash
git clone https://github.com/Efe-The-menace/taskmanager-api.git
cd taskmanager-api
```

### 2. Create & activate a virtual environment
```bash
python -m venv env
# On Linux/Mac
source env/bin/activate
# On Windows
env\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply migrations
```bash
python manage.py migrate
```
### 5. Create a superuser (for admin access)
```bash
python manage.py createsuperuser
```

### 6. Run the development server
```bash
python manage.py runserver
```

## 🔑 Authentication

<b>This API uses JWT Authentication.</b>

### Obtain a token:
```http
POST /api/token/
{
  "username": "your_username",
  "password": "your_password"
}
```

Refresh token:
```http
POST /api/token/refresh/
{
  "refresh": "your_refresh_token"
}
```

Use in requests:
```http
Authorization: Bearer <access_token>
```

## API Endpoints
## Overview

| Method | Endpoint    | Description                |
|--------|-------------|----------------------------|
| GET    | /overview/  | Lists available endpoints  |

## Tasks

| Method | Endpoint         | Description          |
|--------|------------------|----------------------|
| GET    | /api/tasks/      | List all tasks       |
| POST   | /api/tasks/      | Create a new task    |
| GET    | /api/task/pk/  | Retrieve a single task |
| PUT    | /api/task/pk/  | Update a task        |
| DELETE | /api/task/pk/  | Delete a task        |

## Example Task Object
```json
{
  "id": 1,
  "title": "Become The Goat",
  "description": "Work through API authentication section",
  "completed": true,
  "owner": "efe"
}
```
## Permissions

Only authenticated users can access tasks

Users can only modify or delete their own tasks

## Future Improvements
Filtering & searching tasks

Docker setup for easy deployment

