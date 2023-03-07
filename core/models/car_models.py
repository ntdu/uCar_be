import uuid
from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


from .database import engine

car_Base = declarative_base()

class CarBrand(car_Base):
    __tablename__ = 'carbrands'
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False,
                default=uuid.uuid4)
    name = Column(String,  nullable=False)
    logo = Column(String, nullable=True)
    description = Column(String, nullable=True)
    
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))


class CarModel(car_Base):
    __tablename__ = 'carmodels'
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False,
                default=uuid.uuid4)
    carbrand_id = Column(UUID(as_uuid=True), ForeignKey(
        'carbrands.id', ondelete='CASCADE'), nullable=False)
    name = Column(String,  nullable=False)
    logo = Column(String, nullable=True)
    description = Column(String, nullable=True)
    
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    carbrand = relationship('CarBrand')


car_Base.metadata.create_all(engine)
