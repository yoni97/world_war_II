from flask import session
from sqlalchemy import Column, Integer, String, Date, Table, ForeignKey, Index
from sqlalchemy.orm import relationship
from Base.base import Base

class TargetType(Base):
    __tablename__ = 'targettypes'
    target_type_id = Column(Integer, primary_key=True)
    target_type_name = Column(String)