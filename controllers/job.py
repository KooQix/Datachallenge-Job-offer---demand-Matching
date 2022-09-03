from typing import List
from fastapi import APIRouter, Depends, HTTPException
from models.db import Base, SessionLocal, engine
from sqlalchemy.orm import Session
from models.job import repository, schemas


	#################### Config ####################


Base.metadata.create_all(bind=engine)
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(tags=["job"], responses={404: {"ERROR": "Not found"}})



	#################### Routes ####################

       
@router.get("/", response_model=List[schemas.Job])
def get_all(db: Session = Depends(get_db)):
	try:
		return repository.get_all(db)

	except Exception as e:
		raise HTTPException(status_code=404, detail=f"An error occurred while retrieving data: {e}")


@router.get("/{id}", response_model=schemas.Job)
def get_one_by_id(id: int, db: Session = Depends(get_db)):
	try:
		return repository.get_one_by_id(id, db)

	except Exception as e:
		raise HTTPException(status_code=404, detail=f"An error occurred while retrieving data: {e}")

    
@router.post("/", response_model=schemas.Job)
def create(job_create: schemas.JobCreate, db: Session = Depends(get_db)):
	try:
		return repository.create(job_create, db)

	except Exception as e:
		raise HTTPException(status_code=404, detail=f"An error occurred while creating Job: {e}")



@router.delete("/{id}", response_model=schemas.Job)
def delete(id: int, db: Session = Depends(get_db)):
	try:
		return repository.delete(id, db)
	except Exception as e:
		raise HTTPException(status_code=404, detail=f"An error occurred while deleting Job: {e}")