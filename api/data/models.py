from sqlmodel import SQLModel, Field
from pydantic import BaseModel

class UserBase(BaseModel):
    """
    Base model for user data.
    """
    username: str = Field(..., description="The username of the user.")

class UserLogin(UserBase):
    password: str

class UserCreate(UserBase):
    """
    Model for creating a new user.    
    - **password**: The password for the user.
    """
    password: str
    role: str = Field(..., description="The role of the user (e.g., admin, user).")


class UserRead(UserBase):
    """
    Model for reading user data.    
    - **id**: The unique identifier for the user.
    - **role**: The role of the user (e.g., admin, user).
    """
    id: int = Field(..., description="The unique identifier for the user.")
    role: str = Field(..., description="The role of the user (e.g., admin, user).")


class Users(SQLModel, table=True):
    """
    SQLModel representation of a user.    
    - **id**: The unique identifier for the user.
    - **username**: The username of the user.
    - **password**: The hashed password of the user.
    - **role**: The role of the user (default is "user").
    """
    id: int = Field(default=None, primary_key=True,)
    username: str = Field(index=True, unique=True)
    password: str
    role: str = Field(default="user")

class ProjectBase(BaseModel):
    """
    Base model for project data.
    
    - **name**: The name of the project.
    - **description**: A brief description of the project.
    """
    name: str
    description: str

class ProjectCreate(ProjectBase):
    """
    Model for creating a new project.
    """
    pass

class ProjectRead(ProjectBase):
    """
    Model for reading project data.    
    - **id**: The unique identifier for the project.
    """
    id: int = Field(..., description="The unique identifier for the project.")


class Projects(SQLModel, table=True):
    """
    SQLModel representation of a project.    
    - **id**: The unique identifier for the project.
    - **name**: The name of the project.
    - **description**: A brief description of the project.
    """
    id: int = Field(default=None, primary_key=True, description="The unique identifier for the project.")
    name: str = Field(index = True, unique=True, description="The name of the project.")
    description: str = Field(..., description="A brief description of the project.")
