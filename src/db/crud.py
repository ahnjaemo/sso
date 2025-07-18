from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from . import models
from ..schemas.schemas import UserCreate, UserResponse
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.User).filter(models.User.email == email))
    return result.scalars().first()

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(models.User).offset(skip).limit(limit))
    return result.scalars().all()

async def create_user(db: AsyncSession, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        provider="local",
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def create_oauth_user(db: AsyncSession, user_info: dict):
    db_user = models.User(
        email=user_info["email"],
        full_name=user_info["name"],
        provider="google",
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user