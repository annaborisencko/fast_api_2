from typing import Literal
import datetime

from pydantic import BaseModel, Field
from .custom_types import ROLE


class IdResponse(BaseModel):
    id: int


class SuccessResponse(BaseModel):
    status: Literal["success"]


class BaseUserRequest(BaseModel):
    name: str
    password: str
    role: ROLE | None = None


class CreateUserRequest(BaseUserRequest):
    pass


class LoginUserRequest(BaseModel):
    name: str
    password: str


class LoginUserResponse(BaseModel):
    # token: uuid.UUID
    token: str


class CreateUserResponse(IdResponse):
    pass


class UpdateUserRequest(BaseUserRequest):
    name: str | None = None
    password: str | None = None
    role: ROLE | None = None


class UpdateUserResponse(SuccessResponse):
    pass


class GetUserResponse(BaseModel):
    id: int
    name: str
    role: ROLE
    registration_time: datetime.datetime


class DeleteUserResponse(SuccessResponse):
    pass


class CreateAdvRequest(BaseModel):
    title: str
    description: str
    price: float = Field(..., gt=0, description="Price must be more than 0")


class CreateAdvResponse(IdResponse):
    pass


class UpdateAdvRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = Field(None, gt=0, description="Price must be more than 0")


class UpdateAdvResponse(SuccessResponse):
    pass


class GetAdvResponse(BaseModel):
    id: int
    title: str
    description: str
    price: float
    user_id: int
    created_at: datetime.datetime


class SearchAdvResponse(BaseModel):
    results: list[GetAdvResponse]


class DeleteAdvResponse(SuccessResponse):
    pass
