from datetime import datetime
import uuid
from .. import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from ..models.database import get_db
from sqlalchemy import text

from ..schemas import schemas

router = APIRouter()

@router.get('/', response_model=schemas.ListCarModelResponse)
def get_carmodels(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''):
    skip = (page - 1) * limit

    carmodels = db.query(models.CarModel).group_by(models.CarModel.id).filter(
        models.CarModel.name.contains(search)).limit(limit).offset(skip).all()
    return {'status': 'success', 'results': len(carmodels), 'carmodels': carmodels}

@router.get('/{id}', response_model=schemas.CarModelResponse)
def get_carmodel(id: str, db: Session = Depends(get_db)):
    carmodel = db.query(models.CarModel).filter(models.CarModel.id == id).first()
    if not carmodel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No carmodel with this id: {id} found")
    return carmodel

@router.get('/carbrands/{carbrand_id}', response_model=schemas.ListCarModelResponse)
def get_carmodel_by_carbrand(carbrand_id: str, db: Session = Depends(get_db), limit: int = 10, page: int = 1):
    skip = (page - 1) * limit

    carbrand = db.query(models.CarBrand).filter(models.CarBrand.id == carbrand_id).first()
    if not carbrand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No carbrand with this id: {carbrand_id} found")

    carmodels = db.query(models.CarModel).filter(
        models.CarModel.carbrand_id == carbrand_id).limit(limit).offset(skip).all()
    return {'status': 'success', 'results': len(carmodels), 'carmodels': carmodels}

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.CarModelResponse)
def create_carmodel(carmodel: schemas.CarModelBaseSchema, db: Session = Depends(get_db)):
    carbrand = db.query(models.CarBrand).filter(models.CarBrand.id == carmodel.carbrand_id).first()
    if not carbrand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No carbrand with this id: {carmodel.carbrand_id} found")

    new_carmodel = models.CarModel(**carmodel.dict())
    db.add(new_carmodel)
    db.commit()
    db.refresh(new_carmodel)
    return new_carmodel

@router.put('/{id}', response_model=schemas.CarModelResponse)
def update_carmodel(id: str, carmodel: schemas.UpdateCarModelSchema, db: Session = Depends(get_db)):
    if carmodel.carbrand_id:
        carbrand = db.query(models.CarBrand).filter(models.CarBrand.id == carmodel.carbrand_id).first()
        if not carbrand:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No carbrand with this id: {carmodel.carbrand_id} found")

    carmodel_query = db.query(models.CarModel).filter(models.CarModel.id == id)
    updated_carmodel = carmodel_query.first()

    if not updated_carmodel:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f'No carmodel with this id: {id} found')

    carmodel_query.update(carmodel.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return updated_carmodel

@router.delete('/{id}')
def delete_carmodel(id: str, db: Session = Depends(get_db)):
    carmodel_query = db.query(models.CarModel).filter(models.CarModel.id == id)
    carmodel = carmodel_query.first()
    if not carmodel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No carmodel with this id: {id} found')

    carmodel_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)