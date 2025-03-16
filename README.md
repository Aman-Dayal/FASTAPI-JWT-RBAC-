# FastAPI Project with JWT Authentication and Role-Based Access Control (RBAC)

## Overview
This project implements a RESTful API using FastAPI with JWT authentication and Role-Based Access Control (RBAC). The API manages user registration, authentication, and project management.

## Features
- User registration and authentication
- Role-based access control
- CRUD operations for projects
- Interactive API documentation

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Aman-Dayal/FASTAPI-JWT-RBAC-.git
   cd FASTAPI-JWT-RBAC
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database (update the database URL in env ):
   ```bash
   # Example for PostgreSQL
   DATABASE_URL="postgresql://user:password@localhost/dbname"
   ```
5. Add environment variables to the .env file:
   SECRET_KEY : for jwt authentication
   API_KEY : for api key authentication

6. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

## API Documentation
The API documentation can be accessed at:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Endpoints
### User Endpoints
- `POST /users/register`: Register a new user
- `POST /users/login`: Authenticate a user

### Project Endpoints
- `POST /projects`: Create a new project
- `GET /projects`: Retrieve all projects
- `GET /projects/{project_id}`: Retrieve a specific project
- `PUT /projects/{project_id}`: Update an existing project
- `DELETE /projects/{project_id}`: Delete a project

## Tech Stack
- FastAPI
- PostgreSQL
- SQLModel
- bcrypt
- PyJWT

## Additional Configurations
- Ensure PostgreSQL is running and accessible.
- Update any necessary environment variables for JWT secret keys and database connection.
