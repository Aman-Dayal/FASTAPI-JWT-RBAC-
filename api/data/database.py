from sqlmodel import SQLModel, create_engine, Session
from api.common.settings import settings
from api.common.logger import logger

engine = create_engine(settings.database_url, echo=True, pool_size=20, max_overflow=0)

def on_startup():
    """Initialize database schema on application startup."""
    try:
        SQLModel.metadata.create_all(engine)
        logger.info("Database schema initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing database schema: {e}", exc_info=True)
        raise

def get_session():
    """Dependency to provide a database session."""
    with Session(engine) as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Database session error: {e}", exc_info=True)
            raise
        finally:
            session.close()