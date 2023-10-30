from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base

###
### This file contains SQLAlchemy model of the database
###

class Tile(Base):
    __tablename__ = 'tiles'

    tile_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    # TODO Maybe add some more attributes to the tiles?

    # Define one-to-many relationship with the DataFrame table
    data_frames = relationship('DataFrame', back_populates='tile')


class DataFrame(Base):
    __tablename__ = 'data_frame'

    data_id = Column(Integer, primary_key=True)
    tile_id = Column(Integer, ForeignKey('tiles.tile_id'))
    timestamp = Column(DateTime, server_default=func.now())
    voltage = Column(Float)
    steps = Column(Integer)                 

    # Define one-to-many relationship with the Tile table
    tile = relationship('Tile', back_populates='data_frames')