from typing import List
from fastapi import APIRouter, Depends, HTTPException
from models.client import schemas, repository
from models.jober import schemas as jober_schemas
from models.db import Base, SessionLocal, engine
from sqlalchemy.orm import Session

from app.find_jober import get_best_match_client

	#################### Config ####################


Base.metadata.create_all(bind=engine)
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(tags=["client"], responses={404: {"ERROR": "Not found"}})



	#################### Routes ####################

        
@router.get("/", response_model=List[schemas.Client])
def get_all(db: Session = Depends(get_db)):
	try:
		return repository.get_all(db)

	except Exception as e:
		raise HTTPException(status_code=404, detail=f"An error occurred while retrieving data: {e}")


@router.get("/{id}", response_model=schemas.Client)
def get_one_by_id(id: int, db: Session = Depends(get_db)):
	try:
		return repository.get_one_by_id(id, db)

	except Exception as e:
		raise HTTPException(status_code=404, detail=f"An error occurred while retrieving data: {e}")


# Return the list of the best match
@router.get("/best_match/{client_id}", response_model=List[jober_schemas.JoberMatch])
def get_best_match(client_id: int, db: Session = Depends(get_db)):
	try:
		client = repository.get_one_by_id(client_id, db)
		# Matching logic to find the best jobers matched for client_id client
		return get_best_match_client(client)
	except Exception as e:
		raise HTTPException(status_code=404, detail=f"An error occurred while retrieving data: {e}")


    
@router.post("/", response_model=schemas.Client)
def create(client: schemas.ClientCreate, db: Session = Depends(get_db)):
	try:
		return repository.create(client, db)

	except Exception as e:
		raise HTTPException(status_code=404, detail=f"An error occurred while creating client: {e}")


@router.patch("/{id}", response_model=schemas.Client)
def update(id: int, client: schemas.ClientUpdate, db: Session = Depends(get_db)):
	try:
		return repository.update(id, client, db)

	except Exception as e:
		raise HTTPException(status_code=404, detail=f"An error occurred while updating client: {e}")



@router.delete("/{id}", response_model=schemas.Client)
def delete(id: int, db: Session = Depends(get_db)):
	try:
		return repository.delete(id, db)
	except Exception as e:
		raise HTTPException(status_code=404, detail=f"An error occurred while deleting client: {e}")