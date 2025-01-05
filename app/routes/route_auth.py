from fastapi import APIRouter, FastAPI, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
import httpx
import os
from auth0.authentication import Database
from auth0.authentication import GetToken
from app.schemas import user_schema
from auth0.authentication.token_verifier import TokenVerifier, AsymmetricSignatureVerifier


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


@router.post("/register")
async def register(user:user_schema.UserCreate):

    database = Database(AUTH0_DOMAIN, AUTH0_CLIENT_ID)
    #database.signup(email='s', password='secr@bqqAs83t', connection='Username-Password-Authentication')
    try:
        new_user=database.signup(
            connection= 'Username-Password-Authentication',  
            username= user.username, 
            password= user.password,
            email=user.email
    
        )

    except Exception as ex:
        print(ex)
        raise HTTPException (status_code=400,detail=str(ex))
    print(new_user)
    return user_schema.User(user_id=new_user["_id"],username=user.username,email=user.email)


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
