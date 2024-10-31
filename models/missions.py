from flask import session
from sqlalchemy import Column, Integer, String, Date, Table, ForeignKey, Index, Float
from sqlalchemy.orm import relationship
from database.db import Base

class MissionModel(Base):
    __tablename__ = 'missions'
    mission_id = Column(Integer, primary_key=True)
    mission_date = Column(Date)
    airborne_aircraft = Column(Float)
    attacking_aircraft = Column(Float)
    bombing_aircraft = Column(Float)
    aircraft_returned = Column(Float)
    aircraft_failed = Column(Float)
    aircraft_damaged = Column(Float)
    aircraft_lost = Column(Float)

    targets = relationship("TargetModel", back_populates="mission")


