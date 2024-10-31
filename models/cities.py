from flask import session
from sqlalchemy import Column, Integer, String, Table, ForeignKey, Index
from sqlalchemy.orm import relationship
from Base.base import Base

class City(Base):
    __tablename__ = 'cities'
    city_id = Column(Integer, primary_key=True)
    city_name = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    country_id = Column(Integer, ForeignKey('countries.country_id'))
    country = relationship('Country', back_populates='cities')
