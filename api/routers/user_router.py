from fastapi import APIRouter, HTTPException, Depends
from api.common.logger import logger
from sqlmodel import Session, select
from api.data.models import Users, UserCreate, UserBase, UserLogin
from api.data.database import get_session
from api.common.security import create_jwt_token, verify_password, hash_password
from sqlalchemy.exc import IntegrityError

router = APIRouter()

@router.post("/register", response_model=UserBase, summary="Register a new user",
description="This endpoint allows a new user to register by providing a username and password.")
def register(user: UserCreate, session: Session = Depends(get_session)):
    """
    Registers a new user by providing a username and password.    
    - **user**: The user information for registration.    
    Returns the created user information.
    """
    try:
        user.password = hash_password(user.password)
        db_user = Users.model_validate(user)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        logger.info(f"User registered successfully: {db_user.username}")
        return db_user
    except IntegrityError:
        session.rollback()
        logger.error("User registration failed: User already exists.")
        raise HTTPException(status_code=400, detail="User already exists.")
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="An error Occured!")
    
@router.post("/login", summary="User login", response_model = dict,
description="This endpoint allows a user to log in by providing their username and password.")
def login(user: UserLogin, session: Session = Depends(get_session)):

    """
    Allows a user to log in by providing their username and password.    
    - **user**: The user credentials for login.    
    Returns an access token if the credentials are valid.
    """
    db_user = session.exec(select(Users).where(Users.username == user.username)).first()
    if not db_user or not verify_password(user.password, db_user.password):
        logger.warning(f"Login attempt failed for user: {user.username}")
        raise HTTPException(status_code=400, detail="Invalid credentials")
    logger.info(f"User logged in successfully: {db_user.username}")

    access_token = create_jwt_token({"sub": db_user.username, "role": db_user.role})
    return {"access_token": access_token}
