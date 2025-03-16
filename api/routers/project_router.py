from fastapi import APIRouter, HTTPException, Depends
from api.common.logger import logger

from sqlmodel import Session, select
from api.data.models import *
from api.data.database import get_session
from api.common.security import get_current_user
from typing import List, Union
from sqlalchemy.exc import IntegrityError

router = APIRouter()

@router.post("/", response_model=ProjectRead, summary="Create a new project", description="Create a new project with the provided details.")
def create_project(project: ProjectCreate, session: Session = Depends(get_session), current_user: Users = Depends(get_current_user)):
    """
    Create a new project.
    - **project**: The project details to create.
    - **session**: The database session.
    - **current_user**: The user making the request.
    Returns the created project.
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    try:
        logger.info(f"Creating project: {project.name}")
        db_project = Projects.model_validate(project)
        session.add(db_project)
        session.commit()
        session.refresh(db_project)
        return db_project
    except IntegrityError:
        session.rollback()
        logger.error("Project creation failed: Project with this name already exists.")
        raise HTTPException(status_code=400, detail="Project with this name already exists.")
    except Exception as e:
        session.rollback()
        logger.error(f"Project creation failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create project")
    
@router.get("/{project_id}", response_model=Union[ProjectBase,ProjectRead], summary="Get a specific project", description="Retrieve a specific project by its ID.")
def get_project(project_id: int, session: Session = Depends(get_session), current_user: Users = Depends(get_current_user)):
    """
    Retrieve a specific project by its ID.
    - **project_id**: The ID of the project to retrieve.
    - **session**: The database session.
    Returns the requested project.
    """
    db_project = session.get(Projects, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    if current_user.role != "admin":
        return ProjectRead.model_validate(db_project.model_dump())
    return ProjectBase.model_validate(db_project.model_dump())
    
@router.put("/{project_id}", response_model=ProjectBase, summary="Update an existing project", description="Update the details of an existing project.")
def update_project(project_id: int, project: ProjectCreate, session: Session = Depends(get_session), current_user: Users = Depends(get_current_user)):
    """
    Update an existing project.
    - **project_id**: The ID of the project to update.
    - **project**: The updated project details.
    - **session**: The database session.
    - **current_user**: The user making the request.
    Returns the updated project.
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    db_project = session.get(Projects, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    logger.info(f"Updating project: {project_id} with new details.")
    db_project.name = project.name
    db_project.description = project.description
    session.commit()
    session.refresh(db_project)
    return db_project

@router.delete("/{project_id}", response_model=dict, summary="Delete a project", description="Delete a project by its ID.")
def delete_project(project_id: int, session: Session = Depends(get_session), current_user: Users = Depends(get_current_user)):
    """
    Delete a project by its ID.
    - **project_id**: The ID of the project to delete.
    - **session**: The database session.
    - **current_user**: The user making the request.
    Returns a confirmation message.
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    logger.info(f"Deleting project with ID: {project_id}")
    db_project = session.get(Projects, project_id)
    if not db_project:
        logger.warning(f"Project with ID {project_id} not found for deletion.")
        raise HTTPException(status_code=404, detail="Project not found")
    session.delete(db_project)
    session.commit()
    return {"detail": "Project deleted successfully"}

@router.get(
    "/",
    response_model=Union[List[ProjectBase], List[ProjectRead]],
    summary="Get all projects",
    description="Retrieve a list of all projects.",
)
def get_projects(
    session: Session = Depends(get_session), 
    current_user: Users = Depends(get_current_user)
):
    """
    Retrieve a list of all projects.
    - **session**: The database session.
    - **current_user**: The authenticated user.
    Returns a list of projects.
    """
    logger.info("Retrieving all projects.")
    projects = session.scalars(select(Projects)).all()
    if current_user.role == "admin":
        return [ProjectRead.model_validate(p.model_dump()) for p in projects]
    return [ProjectBase.model_validate(p.model_dump()) for p in projects]
