from fastapi import FastAPI
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from .schema import (
    CreateUserRequest,
    CreateUserResponse,
    UpdateUserRequest,
    UpdateUserResponse,
    GetUserResponse,
    DeleteUserResponse,
    LoginUserRequest,
    LoginUserResponse,
    CreateAdvRequest,
    CreateAdvResponse,
    DeleteAdvResponse,
    GetAdvResponse,
    SearchAdvResponse,
    UpdateAdvRequest,
    UpdateAdvResponse,
)
from .lifespan import lifespan
from .dependency import SessionDependency, TokenDependency
from .constants import SUCCESS_RESPONSE
from . import models
from . import crud
from .auth import generate_token, check_password, hash_password


import datetime

app = FastAPI(title="Adv API", lifespan=lifespan)


@app.post("/api/v1/user", tags=["user"], response_model=CreateUserResponse)
async def create_user(user_data: CreateUserRequest, session: SessionDependency):
    user_dict = user_data.model_dump(exclude_unset=True)
    user_dict["password"] = hash_password(user_data.password)
    user_orm_obj = models.User(**user_dict)
    await crud.add_item(session, user_orm_obj)
    return user_orm_obj.id_dict


@app.get("/api/v1/user/{user_id}", response_model=GetUserResponse)
async def get_user(user_id: int, session: SessionDependency):
    user_orm_obj = await crud.get_item_by_id(session, models.User, user_id)
    return user_orm_obj.dict


@app.patch("/api/v1/user/{user_id}", response_model=UpdateUserResponse)
async def update_user(
    user_id: int, user_data: UpdateUserRequest, session: SessionDependency, token: TokenDependency
):
    user_dict = user_data.model_dump(exclude_unset=True)
    if user_dict.get("password"):
        user_dict["password"] = hash_password(user_data.password)
    user_orm_obj = await crud.get_item_by_id(session, models.User, user_id)
    # if token.user.role == "admin" or token.user_id == user_orm_obj.id:
    if token.role == "admin" or token.id == user_orm_obj.id:
        for field, value in user_dict.items():
            setattr(user_orm_obj, field, value)
        try:
            await session.commit()
        except IntegrityError:
            raise HTTPException(409, "Item already exists")
        return SUCCESS_RESPONSE
    raise HTTPException(403, "Insufficient Privileges")


@app.delete("/api/v1/user/{user_id}", response_model=DeleteUserResponse)
async def delete_user(user_id: int, session: SessionDependency, token: TokenDependency):
    user_orm_obj = await crud.get_item_by_id(session, models.User, user_id)
    # if token.user.role == "admin" or token.user_id == user_orm_obj.id:
    if token.role == "admin" or token.id == user_orm_obj.id:
        await crud.delete_item(session, user_orm_obj)
        return SUCCESS_RESPONSE
    raise HTTPException(403, "Insufficient Privileges")


@app.post("/api/v1/login", tags=["login"], response_model=LoginUserResponse)
async def login(login_data: LoginUserRequest, session: SessionDependency):
    query = select(models.User).where(models.User.name == login_data.name)
    user = await session.scalar(query)
    if user is None:
        raise HTTPException(401, "Invalid credentials")
    if not check_password(login_data.password, user.password):
        raise HTTPException(401, "Invalid credentials")
    # token = models.Token(user_id=user.id)
    token = generate_token(user_data={"user_id": user.id, "username": user.name, "role": user.role})
    return {"token": token}
    # await crud.add_item(session, token)
    # return token.dict


@app.post("/api/v1/advertisement", response_model=CreateAdvResponse)
async def create_adv(Adv: CreateAdvRequest, session: SessionDependency, token: TokenDependency):
    adv_dict = Adv.model_dump(exclude_unset=True)
    adv_orm_obj = models.Adv(**adv_dict, user_id=token.id)
    # if token.user.role == "admin" or token.user_id == adv_orm_obj.user_id:
    if token.role == "admin" or token.id == adv_orm_obj.user_id:
        await crud.add_item(session, adv_orm_obj)
        return adv_orm_obj.id_dict
    raise HTTPException(403, "Insufficient Privileges")


@app.get("/api/v1/advertisement/{adv_id}", response_model=GetAdvResponse)
async def get_adv(adv_id: int, session: SessionDependency):
    adv_orm_obj = await crud.get_item_by_id(session, models.Adv, adv_id)
    return adv_orm_obj.dict


@app.get("/api/v1/advertisement", response_model=SearchAdvResponse)
async def search_adv(
    session: SessionDependency,
    id: int = None,
    title: str = None,
    description: str = None,
    price_min: float = None,
    price_max: float = None,
    user_id: int = None,
    created_at: datetime.datetime = None,
    limit: int = 10,
    offset: int = 0,
):

    if price_min is not None and price_max is not None and price_min > price_max:
        raise HTTPException(400, "price_min must be <= price_max")

    query = select(models.Adv)
    conditions = []

    if id is not None:
        conditions.append(models.Adv.id == id)

    if title is not None:
        conditions.append(models.Adv.title.contains(title))

    if description is not None:
        conditions.append(models.Adv.description.contains(description))

    if price_min is not None:
        conditions.append(models.Adv.price >= price_min)

    if price_max is not None:
        conditions.append(models.Adv.price <= price_max)

    if user_id is not None:
        conditions.append(models.Adv.user_id == user_id)

    if created_at is not None:
        conditions.append(models.Adv.created_at == created_at)

    if conditions:
        query = query.where(*conditions)

    query = query.limit(limit).offset(offset)
    advs = await session.scalars(query)
    return {"results": [adv.dict for adv in advs]}


@app.patch("/api/v1/advertisement/{adv_id}", response_model=UpdateAdvResponse)
async def update_adv(
    adv_id: int, adv_data: UpdateAdvRequest, session: SessionDependency, token: TokenDependency
):
    adv_dict = adv_data.model_dump(exclude_unset=True)
    adv_orm_obj = await crud.get_item_by_id(session, models.Adv, adv_id)
    # if token.user.role == "admin" or token.user_id == adv_orm_obj.user_id:
    if token.role == "admin" or token.id == adv_orm_obj.user_id:
        for field, value in adv_dict.items():
            setattr(adv_orm_obj, field, value)
        try:
            await session.commit()
        except IntegrityError:
            raise HTTPException(409, "Item already exists")
        return SUCCESS_RESPONSE
    raise HTTPException(403, "Insufficient Privileges")


@app.delete("/api/v1/advertisement/{adv_id}", response_model=DeleteAdvResponse)
async def delete_adv(adv_id: int, session: SessionDependency, token: TokenDependency):
    adv_orm_obj = await crud.get_item_by_id(session, models.Adv, adv_id)
    # if token.user.role == "admin" or token.user_id == adv_orm_obj.user_id:
    if token.role == "admin" or token.id == adv_orm_obj.user_id:
        await crud.delete_item(session, adv_orm_obj)
        return SUCCESS_RESPONSE
    raise HTTPException(403, "Insufficient Privileges")
