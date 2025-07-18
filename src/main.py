from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
import httpx
from starlette.responses import RedirectResponse
from starlette.requests import Request
from typing import List
# from google_auth_oauthlib.flow import Flow

from .api import auth
from .db import crud, models
from .db.database import get_db, engine
from .schemas.schemas import UserCreate, UserResponse, Token
from .core import config

app = FastAPI(openapi_extra={
    "components": {
        "securitySchemes": {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            }
        }
    },
    "security": [{
        "BearerAuth": []
    }]
})

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

# Standard Authentication
@app.post("/auth/register", response_model=UserResponse)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(db=db, user=user)

@app.post("/auth/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await crud.get_user_by_email(db, email=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# # Google OAuth2
# flow = Flow.from_client_config(
#     client_config={
#         "web": {
#             "client_id": settings.GOOGLE_CLIENT_ID,
#             "client_secret": settings.GOOGLE_CLIENT_SECRET,
#             "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#             "token_uri": "https://oauth2.googleapis.com/token",
#             "redirect_uris": ["http://localhost:8000/auth/google/callback"],
#         }
#     },
#     scopes=["https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile", "openid"],
#     redirect_uri="http://localhost:8000/auth/google/callback"
# )

# @app.get("/auth/google/login")
# async def google_login():
#     authorization_url, state = flow.authorization_url(
#         access_type="offline",
#         include_granted_scopes="true"
#     )
#     return RedirectResponse(authorization_url)

# @app.get("/auth/google/callback")
# async def google_callback(request: Request, db: AsyncSession = Depends(get_db)):
#     flow.fetch_token(authorization_response=str(request.url))
#     credentials = flow.credentials

#     async with httpx.AsyncClient() as client:
#         user_info_res = await client.get(
#             "https://www.googleapis.com/oauth2/v1/userinfo",
#             headers={"Authorization": f"Bearer {credentials.token}"}
#         )
#     user_info = user_info_res.json()
#     email = user_info.get("email")

#     user = await crud.get_user_by_email(db, email=email)
#     if not user:
#         user = await crud.create_oauth_user(db, user_info)

#     access_token = auth.create_access_token(data={"sub": user.email})
#     return {"access_token": access_token, "token_type": "bearer"}

# Protected Endpoint
@app.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

@app.get("/users", response_model=List[UserResponse])
async def read_users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    users = await crud.get_users(db, skip=skip, limit=limit)
    return users
