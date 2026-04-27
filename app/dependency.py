from typing import Annotated
from fastapi import Depends, HTTPException
from .models import Session, User
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .auth import decode_token

security = HTTPBearer()


async def get_session() -> AsyncSession:
    async with Session() as session:
        yield session


SessionDependency = Annotated[AsyncSession, Depends(get_session)]


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session),
) -> User:

    if credentials is None:
        raise HTTPException(401, "Not authenticated")

    token = credentials.credentials

    user_data = decode_token(token)
    if user_data is None:
        raise HTTPException(401, "Invalid or expired token")

    user_id = user_data.get("user_id")
    if user_id is None:
        raise HTTPException(401, "Invalid token payload")

    user = await session.get(User, user_id)
    if user is None:
        raise HTTPException(401, "User not found")

    return user


TokenDependency = Annotated[User, Depends(get_current_user)]
