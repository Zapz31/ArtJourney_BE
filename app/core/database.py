import logging
from fastapi import HTTPException, status
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from app.core.config import settings

logger = logging.getLogger(__name__)
@contextmanager
def get_db_cursor():
    try:
        # Attempt to establish a connection to the database
        conn = psycopg2.connect(settings.DATABASE_URL)
        logger.info("Database connection established successfully.")
    except Exception as e:
        logger.error(f"Failed to connect to the database: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to connect to the database"
        )

    try:
        # RealDictCursor returns results as dictionaries instead of tuples
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            yield cursor
            conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error(f"Database error occurred: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed"
        )
    finally:
        conn.close()
        logger.info("Database connection closed.")