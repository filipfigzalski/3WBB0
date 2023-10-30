from sqlalchemy.orm import Session

import models, schemas

###
### This file handles database operations.
###

def get_tile(db: Session, tile_id: int):
    return db \
            .query(models.Tile) \
            .filter(models.Tile.tile_id == tile_id) \
            .first()

def get_tiles(db: Session, skip: int = 0, limit: int = 100):
    return db \
            .query(models.Tile) \
            .offset(skip) \
            .limit(limit) \
            .all()

def create_tile(db: Session, tile: schemas.TileCreate):
    db_tile = models.Tile(name=tile.name)
    db.add(db_tile)
    db.commit()
    db.refresh(db_tile)
    return db_tile

def get_last_data_frame(db: Session, tile_id: int):
    return db \
            .query(models.DataFrame) \
            .filter(models.DataFrame.tile_id == tile_id) \
            .order_by(models.DataFrame.timestamp.desc()) \
            .first()

def get_last_data_frames(db: Session, tile_id: int, limit: int = 100):
    return db \
            .query(models.DataFrame) \
            .filter(models.DataFrame.tile_id == tile_id) \
            .order_by(models.DataFrame.tile_id.desc()) \
            .limit(limit) \
            .all()

def create_data_frame(db: Session, data_frame: schemas.DataFrameCreate, tile_id: int):
    db_data_frame = models.DataFrame(**data_frame.dict(), tile_id=tile_id)
    db.add(db_data_frame)
    db.commit()
    db.refresh(db_data_frame)
    return db_data_frame

def delete_all_data_frames_of_tile(db: Session, tile_id: int):
    count = db \
            .query(models.DataFrame) \
            .filter(models.DataFrame.tile_id == tile_id) \
            .delete()
    db.commit()
    return count
