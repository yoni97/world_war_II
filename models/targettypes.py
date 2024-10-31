from flask import session
from sqlalchemy import Column, Integer, String, Date, Table, ForeignKey, Index
from sqlalchemy.orm import relationship
from database.db import Base

class TargetTypeModel(Base):
    __tablename__ = 'targettypes'
    target_type_id = Column(Integer, primary_key=True)
    target_type_name = Column(String)

    targets_type = relationship("TargetModel", back_populates="target_type")
