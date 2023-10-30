from pydantic import BaseModel
from datetime import datetime

###
### This file conatains Pydantic models
###

class DataFrameBase(BaseModel):
    voltage: float
    steps: int

class DataFrameCreate(DataFrameBase):
    pass

class DataFrame(DataFrameBase):
    data_id: int
    tile_id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class TileBase(BaseModel):
    name: str

class TileCreate(TileBase):
    pass

class Tile(TileBase):
    tile_id: int
    data_frames: list[DataFrame]

    class Config:
        from_attributes = True

