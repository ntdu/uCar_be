from datetime import datetime
from typing import List
import uuid
from pydantic import BaseModel, EmailStr, constr


class CarBrandBaseSchema(BaseModel):
    name: str
    logo: str | None = None
    description: str | None = None

    class Config:
        orm_mode = True


class CreateCarBrandSchema(CarBrandBaseSchema):
    pass


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class CarBrandResponse(CarBrandBaseSchema):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class FilteredCarBrandResponse(CarBrandBaseSchema):
    id: uuid.UUID


class CarModelBaseSchema(BaseModel):
    name: str
    carbrand_id: uuid.UUID
    logo: str | None = None
    description: str | None = None

    class Config:
        orm_mode = True


class CreateCarModelSchema(CarModelBaseSchema):
    pass


class CarModelResponse(CarModelBaseSchema):
    id: uuid.UUID
    carbrand: FilteredCarBrandResponse
    created_at: datetime
    updated_at: datetime


class UpdateCarModelSchema(BaseModel):
    name: str
    logo: str | None = None
    description: str | None = None

    carbrand_id: uuid.UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


class ListCarModelResponse(BaseModel):
    status: str
    results: int
    carmodels: List[CarModelResponse]


