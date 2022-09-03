from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.jober.entity import JoberEntity
from models.jober.schemas import *

        

def get_all(db: Session):
	"""Get all Jobers

	Args:
		db (Session): Db session

	Returns:
		List[JoberEntity]: The list of jobers in database
	"""
	return db.query(JoberEntity).all()



def get_one_by_id(id: int, db: Session):
	"""Get jober by id

	Args:
		db (Session): Db session
		id (int): Jober id

	Returns:
		JoberEntity: The jober 
	"""
	return db.query(JoberEntity).get(id)



def create(jober_create: JoberCreate, db: Session):
	"""Create jober

	Args:
		db (Session): Db Session
		jober_create (JoberCreate): Jober's information

	Returns:
		JoberEntity: Jober created
	"""
	jober = JoberEntity(jober_create)
	db.add(jober)
	db.commit()
	db.refresh(jober)
	return jober



def update(id: int, jober_update: JoberUpdate, db: Session):
	"""Update a jober

	Args:
		db (Session): Db Session
		jober_update (JoberUpdate): The jober information to update

	Raises:
		HTTPException: 

	Returns:
		JoberEntity: The jober updated
	"""
	jober: JoberEntity = get_one_by_id(id, db)
	if not jober:
		raise HTTPException(status_code=404, detail="Jober does not exist")

	jober = jober.update(jober_update)
	db.commit()
	db.refresh(jober)
	return jober
	
 
 
def delete(id: int, db: Session):
	"""Delete a jober

	Args:
		db (Session): Db Session
		id (int): Jober id

	Raises:
		HTTPException: 

	Returns:
		JoberEntity: Jober deleted
	"""
	jober = get_one_by_id(id, db)
	if not jober:
		raise HTTPException(status_code=404, detail="Jober does not exist")

	db.delete(jober)
	db.commit()
	return jober
