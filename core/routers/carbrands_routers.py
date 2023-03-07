from datetime import datetime
import uuid
from .. import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from ..models.database import get_db
from sqlalchemy import text

from ..schemas import schemas

router = APIRouter()


@router.get('/', response_model=schemas.ListCarBrandResponse)
def get_carbrands(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''):
    skip = (page - 1) * limit

    carbrands = db.query(models.CarBrand).group_by(models.CarBrand.id).filter(
        models.CarBrand.name.contains(search)).limit(limit).offset(skip).all()
    return {'status': 'success', 'results': len(carbrands), 'carbrands': carbrands}

@router.get('/{id}', response_model=schemas.CarBrandResponse)
def get_carbrand(id: str, db: Session = Depends(get_db)):
    carbrand = db.query(models.CarBrand).filter(models.CarBrand.id == id).first()
    if not carbrand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No carbrand with this id: {id} found")
    return carbrand

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.CarBrandResponse)
def create_carbrand(carbrand: schemas.CreateCarBrandSchema, db: Session = Depends(get_db)):
    new_carbrand = models.CarBrand(**carbrand.dict())
    db.add(new_carbrand)
    db.commit()
    db.refresh(new_carbrand)
    return new_carbrand

@router.put('/{id}', response_model=schemas.CarBrandResponse)
def update_carbrand(id: str, carbrand: schemas.UpdateCarBrandSchema, db: Session = Depends(get_db)):
    carbrand_query = db.query(models.CarBrand).filter(models.CarBrand.id == id)
    updated_carbrand = carbrand_query.first()

    if not updated_carbrand:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f'No cardbrand with this id: {id} found')

    carbrand_query.update(carbrand.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return updated_carbrand

@router.delete('/{id}')
def delete_carbrand(id: str, db: Session = Depends(get_db)):
    carbrand_query = db.query(models.CarBrand).filter(models.CarBrand.id == id)
    carbrand = carbrand_query.first()
    if not carbrand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No carbrand with this id: {id} found')

    carbrand_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

