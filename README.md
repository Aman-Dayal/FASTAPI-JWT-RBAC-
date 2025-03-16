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
   git clone <repository-url>
   cd <repository-directory>
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

4. Set up the database (update the database URL in `main.py`):
   ```bash
   # Example for PostgreSQL
   DATABASE_URL="postgresql://user:password@localhost/dbname"
   ```

5. Run the application:
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

## License
This project is licensed under the MIT License.


## Overview
This project implements a RESTful API using FastAPI with JWT authentication and Role-Based Access Control (RBAC). The API manages user registration, login, and CRUD operations for resources.

## Tech Stack
- FastAPI
- PostgreSQL
- SQLModel
- bcrypt
- PyJWT

## Installation Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install fastapi[all] sqlmodel psycopg2-binary bcrypt pyjwt
   ```

4. Set up PostgreSQL database and update connection settings in the code.

## Usage
1. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

2. Access the API documentation at `http://127.0.0.1:8000/docs`.

## Endpoints
- **User Registration:** `POST /register`
- **User Login:** `POST /login`
- **Get Projects:** `GET /projects`
- **Create Project (admin only):** `POST /projects`

## Video Demonstration
[Link to video demonstrating setup and usage]

## Additional Configurations
- Ensure PostgreSQL is running and accessible.
- Update any necessary environment variables for JWT secret keys and database connection.
