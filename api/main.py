from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins={"*"},
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/tiles/', response_model=schemas.Tile)
def create_tile(tile: schemas.TileCreate,
                db: Session = Depends(get_db)):
    return crud.create_tile(db=db, tile=tile)

@app.get('/tiles/', response_model=list[schemas.Tile])
def get_tiles(db: Session = Depends(get_db)):
    return crud.get_tiles(db)

@app.get('/tiles/{tile_id}/', response_model=schemas.Tile)
def get_tile(tile_id: int,
             db: Session = Depends(get_db)):
    db_tile = crud.get_tile(db, tile_id=tile_id)
    if db_tile is None:
        raise HTTPException(status_code=404, detail='Tile not found')
    return db_tile

@app.post('/tiles/{tile_id}/dataframes/', response_model=schemas.DataFrame)
def create_data_frame_for_tile(tile_id: int,
                      data_frame: schemas.DataFrameCreate,
                      db: Session = Depends(get_db)):
    
    if crud.get_tile(db, tile_id=tile_id) is None:
        raise HTTPException(status_code=404, detail='Tile not found')
    
    return crud.create_data_frame(db=db,
                                  tile_id=tile_id,
                                  data_frame=data_frame)

@app.get('/tiles/{tile_id}/dataframes/', response_model=list[schemas.DataFrame])
def get_data_frames_of_tile(tile_id: int,
                            db: Session = Depends(get_db)):
    
    if crud.get_tile(db, tile_id=tile_id) is None:
        raise HTTPException(status_code=404, detail='Tile not found')

    return crud.get_last_data_frames(db, tile_id)

@app.delete("/tiles/{tile_id}/dataframes/") # TODO Response model
def delete_all_data_frames_of_tile(tile_id: int,
                                   db: Session = Depends(get_db)):
    
    if crud.get_tile(db, tile_id=tile_id) is None:
        raise HTTPException(status_code=404, detail='Tile not found')
    
    return crud.delete_all_data_frames_of_tile(db=db, 
                                               tile_id=tile_id)

@app.get('/tiles/{tile_id}/dataframes/last', response_model=schemas.DataFrame)
def get_last_data_frame_of_tile(tile_id: int,
                            db: Session = Depends(get_db)):
    
    if crud.get_tile(db, tile_id=tile_id) is None:
        raise HTTPException(status_code=404, detail='Tile not found')
    
    return crud.get_last_data_frame(db, tile_id)