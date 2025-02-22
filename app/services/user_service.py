from fastapi import HTTPException, status
from app.core.database import get_db_cursor
from app.core.security import get_password_hash, verify_password
from app.schemas.request.request import SignupRequest
from app.schemas.user import UserCreate, User
import logging
import uuid

logger = logging.getLogger(__name__)

def get_user(username: str):
    with get_db_cursor() as cursor:
        cursor.execute(
            "SELECT * FROM users WHERE username = %s",
            (username,)
        )
        user = cursor.fetchone()
        return User(**user) if user else None

def get_user_by_email(email: str):
    with get_db_cursor() as cursor:
        cursor.execute(
            "SELECT * FROM users WHERE email = %s",
            (email,)
        )
        user = cursor.fetchone()
        return User(**user) if user else None

def create_user(req: SignupRequest):
    with get_db_cursor() as cursor:
        hashed_password = get_password_hash(req.password)
        cursor.execute("""
            INSERT INTO users (
                id,
                role,
                email,
                password,
                created_at
            ) VALUES (
		        %s,
                %s,
                %s,
                %s,
                NOW()
            )
            RETURNING id, email, created_at;
        """, (str(uuid.uuid4()), "CUSTOMER", req.email, hashed_password))
        new_user = cursor.fetchone()
        return User(**new_user)

def authenticate_user(email: str, password: str):
    print("email in service: >>>> " + email)
    print("password in service: >>>> " + password)
    try:
        with get_db_cursor() as cursor:
            cursor.execute(
                "select * from users where email = %s",
                (email,)
            )
            user = cursor.fetchone()
            if not user:
                logger.error(f"User not found with email: {email}")
                return False
            if not verify_password(password, user['password']):
                return False
            return User(**user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during authentication"
        )

# Example of more complex queries you might need:
def get_user_stats():
    with get_db_cursor() as cursor:
        cursor.execute("""
            SELECT 
                COUNT(*) as total_users,
                COUNT(CASE WHEN disabled = false THEN 1 END) as active_users,
                COUNT(CASE WHEN disabled = true THEN 1 END) as disabled_users
            FROM users
        """)
        return cursor.fetchone()

def search_users(search_term: str, limit: int = 10):
    with get_db_cursor() as cursor:
        cursor.execute("""
            SELECT id, username, email, full_name, disabled
            FROM users
            WHERE 
                username ILIKE %s OR
                email ILIKE %s OR
                full_name ILIKE %s
            LIMIT %s
        """, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", limit))
        return [User(**user) for user in cursor.fetchall()]