from datetime import datetime
from typing import List
import uuid
from pydantic import BaseModel, EmailStr, constr
from typing import Union


class CarBrandBaseSchema(BaseModel):
    name: str
    logo: Union[str, None] = None
    description: Union[str, None] = None

    class Config:
        orm_mode = True


class CreateCarBrandSchema(CarBrandBaseSchema):
    pass


class CarBrandResponse(CarBrandBaseSchema):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class UpdateCarBrandSchema(BaseModel):
    name: str
    logo: Union[str, None] = None
    description: Union[str, None] = None
    updated_at: datetime

    class Config:
        orm_mode = True


class ListCarBrandResponse(BaseModel):
    status: str
    results: int
    carbrands: List[CarBrandResponse]


class FilteredCarBrandResponse(CarBrandBaseSchema):
    id: uuid.UUID


class CarModelBaseSchema(BaseModel):
    name: str
    carbrand_id: uuid.UUID
    logo: Union[str, None] = None
    description: Union[str, None] = None

    class Config:
        orm_mode = True


class CreateCarModelSchema(CarModelBaseSchema):
    pass


class CarModelResponse(CarModelBaseSchema):
    id: uuid.UUID
    # carbrand: FilteredCarBrandResponse
    created_at: datetime
    updated_at: datetime


class UpdateCarModelSchema(BaseModel):
    name: str
    logo: Union[str, None] = None
    description: Union[str, None] = None

    carbrand_id: Union[uuid.UUID, None] = None
    updated_at: datetime

    class Config:
        orm_mode = True


class ListCarModelResponse(BaseModel):
    status: str
    results: int
    carmodels: List[CarModelResponse]


