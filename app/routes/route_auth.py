from fastapi import APIRouter, FastAPI, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
import httpx
import os
from auth0.authentication import Database
from auth0.authentication import GetToken
from app.schemas import user_schema
from auth0.authentication.token_verifier import TokenVerifier, AsymmetricSignatureVerifier


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from uuid import uuid4
from app.schemas import user_schema  # Assuming user schema is defined
from app.database.database  import SessionLocal,get_db
from app.services.user_service import register_user_in_auth0, save_user_to_db # Assuming your DB session is configured

authrouter = APIRouter(
    tags=["auth"],
)

router = APIRouter()

AUTH0_DOMAIN= "clientuser.us.auth0.com"
AUTH0_CLIENT_ID= "Qx5NEs1NDKrAWdaXUKuX29uXUPtoKh1l"
AUTH0_CLIENT_SECRET= "OIz5jPYdFW-GkskgFWHwZD3ySJto3etbrb-WRU9L-VOV3rkeBPA1Ytv1niEkPivQ"
AUTH0_AUDIENCE= "https://todo-api.com"
ALGORITHMS = ["RS256"]


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_auth0_jwks():
    url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
    response = httpx.get(url)
    response.raise_for_status()
    return response.json()


def decode_jwt(token: str):
    jwks = get_auth0_jwks()
    unverified_header = jwt.get_unverified_header(token)

    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }
    if not rsa_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    try:
        payload = jwt.decode(token, rsa_key, algorithms=ALGORITHMS, audience=AUTH0_AUDIENCE)
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


# @router.post("/register")
# async def register(user:user_schema.UserCreate):

#     database = Database(AUTH0_DOMAIN, AUTH0_CLIENT_ID)
#     #database.signup(email='s', password='secr@bqqAs83t', connection='Username-Password-Authentication')
#     try:
#         new_user=database.signup(
#             connection= 'Username-Password-Authentication',  
#             username= user.username, 
#             password= user.password,
#             email=user.email
    
#         )

#     except Exception as ex:
#         print(ex)
#         raise HTTPException (status_code=400,detail=str(ex))
#     print(new_user)
#     return user_schema.User(user_id=new_user["_id"],username=user.username,email=user.email)


router = APIRouter()


'''@router.post("/register")
async def register(user: user_schema.UserCreate):
    # Initialize the Auth0 Database client
    database = Database(AUTH0_DOMAIN, AUTH0_CLIENT_ID)

    # Register user in Auth0
    try:
        new_user = database.signup(
            connection="Username-Password-Authentication",
            username=user.username,
            password=user.password,
            email=user.email
        )
    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=400, detail=f"Auth0 Registration Error: {str(ex)}")

    # Generate a UUID token for the user
    token = str(uuid4())
    schema_name = f"user_{token}"
    

    # Save user details in your database and create schema
    async with SessionLocal() as session:
        # Check if the user already exists locally
        result = await session.execute(
            text("SELECT 1 FROM public.users WHERE reference_id = :id"),
            {"id": new_user["_id"]}
        )
        if result.fetchone():
            raise HTTPException(status_code=400, detail="User already exists in the database.")

        # Insert user metadata into the public.users table
        await session.execute(
            text("""
                INSERT INTO public.users (reference_id, name, email, uuid)
                VALUES (:reference_id, :name, :email, :uuid)
            """),
            {
                "reference_id": new_user["_id"],
                "name": user.username,
                "email": user.email,
                "uuid": token,
            }
        )

        # Create the user's schema
        await session.execute(text(f'CREATE SCHEMA "{schema_name}"'))

        # Create the tasks table in the new schema
        await session.execute(
            text(f"""
                CREATE TABLE "{schema_name}".tasks (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    description TEXT NOT NULL,
                    completed BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW()
                )
            """)
        )

        # Commit the transaction
        await session.commit()

    # Return the user data along with the token
    return {
        "user_id": new_user["_id"],
        "username": user.username,
        "email": user.email,
        "token": token,
        "message": "User registered successfully!"
    }

'''
# routers/user_router.py
# from fastapi import APIRouter, Depends
# from sqlalchemy.ext.asyncio import AsyncSession
# from app.services.user_service import register_user_in_auth0, save_user_to_db
# from app.database.database import get_db
# from app.schemas import user_schema

router = APIRouter()

@router.post("/register")
async def register(user: user_schema.UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Registers a new user by interacting with Auth0 and the local database.

    Args:
        user (UserCreate): User details from the request body.
        db (AsyncSession): Database session dependency.

    Returns:
        dict: Registered user data with a UUID token.
    """
    # Step 1: Register user in Auth0
    database = Database(AUTH0_DOMAIN, AUTH0_CLIENT_ID)
    new_user = await register_user_in_auth0(
        database=database,
        username=user.username,
        password=user.password,
        email=user.email
    )

    # Step 2: Save user in the local database and create schema
    token = await save_user_to_db(
        session=db,
        reference_id=new_user["_id"],
        username=user.username,
        email=user.email
    )

    # Step 3: Return the response
    return {
        "user_id": new_user["_id"],
        "username": user.username,
        "email": user.email,
        "token": token,
        "message": "User registered successfully!"
    }

''

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    token = GetToken(AUTH0_DOMAIN, AUTH0_CLIENT_ID, client_secret=AUTH0_CLIENT_SECRET)

    user_token=token.login(username=form_data.username, password=form_data.password, realm='Username-Password-Authentication',audience=AUTH0_AUDIENCE)

    return user_token

@router.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):

    domain = AUTH0_DOMAIN
    # client_id =  AUTH0_CLIENT_ID

    print(token)

    jwks_url = 'https://{}/.well-known/jwks.json'.format(domain)
    issuer = 'https://{}/'.format(domain)

    sv = AsymmetricSignatureVerifier(jwks_url) 
    tv = TokenVerifier(signature_verifier=sv, issuer=issuer, audience=AUTH0_AUDIENCE)
    user=tv.verify(token) 
    #user_info = decode_jwt(token)
    print (user)
    return {"message": "Access granted"}
