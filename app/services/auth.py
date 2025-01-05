# from jose import jwt, JWTError
# import requests
# import os

# AUTH0_DOMAIN= "clientuser.us.auth0.com"
# AUTH0_CLIENT_ID= "Qx5NEs1NDKrAWdaXUKuX29uXUPtoKh1l"
# AUTH0_CLIENT_SECRET= "OIz5jPYdFW-GkskgFWHwZD3ySJto3etbrb-WRU9L-VOV3rkeBPA1Ytv1niEkPivQ"
# AUTH0_AUDIENCE= "https://todo-api.com"

# if not all([AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_AUDIENCE]):
#     raise RuntimeError("Auth0 environment variables are missing.")


# class AuthService:
#     @staticmethod
#     def get_access_token(username: str, password: str) -> dict:
#         """Authenticate user and retrieve access token from Auth0."""
#         url = f"https://{AUTH0_DOMAIN}/oauth/token"
#         headers = {"Content-Type": "application/json"}
#         data = {
#             "grant_type": "password",
#             "username": username,
#             "password": password,
#             "audience": AUTH0_AUDIENCE,
#             "client_id": AUTH0_CLIENT_ID,
#             "client_secret": AUTH0_CLIENT_SECRET,
#         }

#         response = requests.post(url, json=data, headers=headers, timeout=10)
#         if response.status_code != 200:
#             error_message = response.json().get("error_description", "Authentication failed")
#             raise ValueError(f"Auth0 Error: {error_message}")

#         return response.json()

#     @staticmethod
#     def verify_token(token: str) -> dict:
#         try:
#             payload = jwt.decode(
#                 token,
#                 key=AUTH0_CLIENT_SECRET,
#                 audience=AUTH0_AUDIENCE,
#                 issuer=f"https://{AUTH0_DOMAIN}/",
#                 algorithms=["RS256"],
#             )
#             return payload
#         except JWTError as e:
#             raise ValueError("Invalid or expired token.") from e