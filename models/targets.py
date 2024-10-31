from flask import session
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class TargetModel(Base):
    __tablename__ = 'targets'
    target_id  = Column(Integer, primary_key=True)
    target_industry = Column(String)
    target_priority = Column(Integer)

    city_id = Column(Integer, ForeignKey('cities.city_id'))
    city = relationship('CityModel', back_populates='targets_city')

    mission_id = Column(Integer, ForeignKey('missions.mission_id'))
    mission = relationship('MissionModel', back_populates='targets')

    target_type_id = Column(Integer, ForeignKey('targettypes.target_type_id'))
    target_type = relationship('TargetTypeModel', back_populates='targets_type')
