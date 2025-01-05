import os
from fastapi import FastAPI
from app.routes.route_user import router as user_router 
from app.routes.route_tasks import router as task_router
from app.routes.route_auth import router as auth_router
# from app.database.database import create_all_tables
app = FastAPI()

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(task_router, prefix="/tasks", tags=["tasks"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])


@app.get("/")
async def root():
    return{"My first FastAPI app"}

# print(f"AUTH0_DOMAIN: {os.getenv('AUTH0_DOMAIN')}")
# print(f"AUTH0_CLIENT_ID: {os.getenv('AUTH0_CLIENT_ID')}")
# print(f"AUTH0_CLIENT_SECRET: {os.getenv('AUTH0_CLIENT_SECRET')}")
# print(f"AUTH0_AUDIENCE: {os.getenv('AUTH0_AUDIENCE')}")



if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="127.0.0.1", port=8000)


# if __name__ == "__main__":
#     create_all_tables() 