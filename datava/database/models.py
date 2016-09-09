__author__ = 'shebashir'

from sqlalchemy import Text, Column, Integer, Numeric, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class JobLocations(Base):
    __tablename__ = 'job_locations'
    id = Column(String(), primary_key=True)
    latitude = Column(String(), nullable=True)
    longitude = Column(String(), nullable=True)
    destination = Column(String(), nullable=True)
    locality = Column(String(), nullable=True)

    job_occupation_categories = relationship("JobOccupationCategories", back_populates="job_locations")


class JobOccupationCategories(Base):
    __tablename__ = 'job_occupation_categories'
    id = Column(String(), primary_key=True)
    occupation_category = Column(String(), nullable=True)
    occupation_broad_category=Column(String(), nullable=True)
    occupation_minor_category=Column(String(), nullable=True)
    occupation_detailed_category=Column(String(), nullable=True)
    job_id = Column(String(), ForeignKey("job_locations.id"))

    job_locations = relationship("JobLocations", back_populates="job_occupation_categories")


#engine = create_engine('sqlite:///C:\\Users\\shebashir\\Desktop\\Datathon\\Data\\job_locations.db')
engine = create_engine('sqlite:///../../job_locations.db')
Base.metadata.create_all(engine)
