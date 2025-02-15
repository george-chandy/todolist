# from sqlalchemy.orm import Session
# from app.models import user_task_models
# from app.schemas import user_schema
# from fastapi import HTTPException
# from app.models.user_task_models import Users

# def create_new_user(db: Session, user_data: user_schema.UserCreate):
#     # if db.query(Users).filter(Users.username == user_data.username).first():
#     #     raise HTTPException(status_code=400, detail="Username already exists")
#     new_user = Users(username=user_data.username)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user

# def get_user_by_id(db: Session, user_id: int):
#     user = db.query(Users).filter(Users.user_id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user

# def get_user_by_username(db: Session, username: str):
#     return db.query(Users).filter(Users.username == username).first()


# services/user_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from uuid import uuid4
from fastapi import HTTPException

async def register_user_in_auth0(database, username: str, password: str, email: str):
    """
    Registers a user in Auth0.
    
    Args:
        database: Auth0 Database client.
        username (str): Username of the user.
        password (str): Password of the user.
        email (str): Email of the user.

    Returns:
        dict: New user details from Auth0.
    """
    try:
        new_user = database.signup(
            connection="Username-Password-Authentication",
            username=username,
            password=password,
            email=email
        )
        return new_user
    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=400, detail=f"Auth0 Registration Error: {str(ex)}")

async def save_user_to_db(session: AsyncSession, reference_id: str, username: str, email: str):
    """
    Save user details in the local database and create a schema.
    
    Args:
        session (AsyncSession): Database session.
        reference_id (str): Auth0 user ID.
        username (str): Username of the user.
        email (str): Email of the user.

    Returns:
        str: The generated UUID token for the user.
    """
    token = str(uuid4())
    schema_name = f"user_{token}"

    # Check if user already exists
    result = await session.execute(
        text("SELECT 1 FROM public.users WHERE reference_id = :id"),
        {"id": reference_id}
    )
    if result.fetchone():
        raise HTTPException(status_code=400, detail="User already exists in the database.")

    # Insert user into the database
    await session.execute(
        text("""
            INSERT INTO public.users (reference_id, name, email, uuid)
            VALUES (:reference_id, :name, :email, :uuid)
        """),
        {
            "reference_id": reference_id,
            "name": username,
            "email": email,
            "uuid": token,
        }
    )

    # Create user's schema
    await session.execute(text(f'CREATE SCHEMA "{schema_name}"'))

    # Create tasks table in the new schema
    await session.execute(
        text(f"""
            CREATE TABLE "{schema_name}".tasks (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                description TEXT NOT NULL,
                completed BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
            )
        """
    )
    )

    # Commit the transaction
    await session.commit()

    return token

