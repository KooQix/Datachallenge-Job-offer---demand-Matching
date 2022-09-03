from typing import List
from fastapi import APIRouter, Depends, HTTPException
from models.jober import schemas, repository
from models.client import schemas as client_schemas
from models.db import Base, SessionLocal, engine
from sqlalchemy.orm import Session

from app.find_client import get_best_match_jober



	#################### Config ####################
 

Base.metadata.create_all(bind=engine)
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(tags=["jober"], responses={404: {"ERROR": "Not found"}})

        


	#################### Routes ####################
 
 
@router.get("/", response_model=List[schemas.Jober])
def get_all(db: Session = Depends(get_db)):
	try:
		return repository.get_all(db)

	except Exception as e:
		raise HTTPException(status_code=404, detail=f"An error occurred while retrieving data: {e}")


@router.get("/{id}", response_model=schemas.Jober)
def get_one_by_id(id: int, db: Session = Depends(get_db)):
	try:
		return repository.get_one_by_id(id, db)

	except Exception as e:
		raise HTTPException(status_code=404, detail=f"An error occurred while retrieving data: {e}")


# Return the list of the best match
@router.get("/best_match/{jober_id}", response_model=List[client_schemas.ClientMatch])
def get_best_match(jober_id: int, db: Session = Depends(get_db)):
	try:
		jober = repository.get_one_by_id(jober_id, db)
		# Matching logic to find the best clients matched for jober_id jober
		return get_best_match_jober(jober)
	except Exception as e:
		raise HTTPException(status_code=404, detail=f"An error occurred while retrieving data: {e}")
		
    
@router.post("/", response_model=schemas.Jober)
def create(jober: schemas.JoberCreate, db: Session = Depends(get_db)):
	try:
		return repository.create(jober, db)

	except Exception as e:
		raise HTTPException(status_code=404, detail=f"An error occurred while creating jober: {e}")


@router.patch("/{id}", response_model=schemas.Jober)
def update(id: int, jober: schemas.JoberUpdate, db: Session = Depends(get_db)):
	try:
		return repository.update(id, jober, db)

	except Exception as e:
		raise HTTPException(status_code=404, detail=f"An error occurred while updating jober: {e}")


@router.delete("/{id}", response_model=schemas.Jober)
def delete(id: int, db: Session = Depends(get_db)):
	try:
		return repository.delete(id, db)
	except Exception as e:
		raise HTTPException(status_code=404, detail=f"An error occurred while deleting jober: {e}")