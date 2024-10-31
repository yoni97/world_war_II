from flask import session
from sqlalchemy import Column, Integer, String, Date, Table, ForeignKey, Index
from sqlalchemy.orm import relationship
from Base.base import Base

class Target(Base):
    __tablename__ = 'targets'
    target_id  = Column(Integer, primary_key=True)
    mission_id = Column(Integer, ForeignKey('missions.mission_id'))
    mission = relationship('Mission', back_populates='targets')
    target_industry = Column(String)
    city_id = Column(Integer, ForeignKey('cities.city_id'))
    city = relationship('City', back_populates='targets')
    target_type_id = Column(Integer, ForeignKey('targettypes.target_type_id'))
    target_type = relationship('TargetType', back_populates='targets')
    target_priority = Column(Integer)
