from sqlalchemy.orm import Session
from models.db import Base, SessionLocal, engine
from fastapi import HTTPException

from models.location.entity import LocationEntity
from models.location.schemas import LocationCreate




def get_all(db: Session):
	"""Get all locations in the database

	Args:
		db (Session): Db Session

	Returns:
		list[LocationEntity]: The list of all locations in the database
	"""
	return db.query(LocationEntity).all()



def get_one_by_id(id: int, db: Session):
	"""Get one location by id

	Args:
		id (int): Location's id
		db (Session): Db Session

	Returns:
		LocationEntity: The location with id = id
	"""
	return db.query(LocationEntity).get(id)


def get_one_by_name(city: str, db: Session, country = "France"):
	"""Get one location by name

	Args:
		city (str): The name of the city
		db (Session): Db Session
		country (str, optional): The country of the location. Defaults to "France".

	Returns:
		LocationEntity | None: The location where city = city
	"""
	res: list[LocationEntity] = db.query(LocationEntity).all()
	for element in res:
		if (element.city.lower() == city.lower()) and (element.country.lower() == country.lower()):
			return element

	return None


def get_or_create(city: str, country = "France"):
	"""Create location if doesn't already exist

	Args:
		city (str): The city to get or create
		country (str, optional): The country of the location. Defaults to "France".

	Returns:
		LocationEntity: The location
	"""
	Base.metadata.create_all(bind=engine)
	db: Session = SessionLocal()

	location = get_one_by_name(city, db, country=country)

	# Doesn't exist => create it
	if (location == None):
		location_create = LocationCreate(city = city, country = country)
		location = create(location_create, db)

	db.close()
	return location


def create(location_create: LocationCreate, db: Session):
	"""Create a new location

	Args:
		location_create (LocationCreate): The location to create
		db (Session): Db Session

	Returns:
		LocationEntity: The location created
	"""
	location = LocationEntity(location_create.city, location_create.country)
	db.add(location)
	db.commit()
	db.refresh(location)
	return location



def delete(id: int, db: Session):
	"""Delete a location from the database

	Args:
		id (int): The id of the location to delete
		db (Session): Db Session

	Raises:
		HTTPException: 

	Returns:
		LocationEntity: The deleted location
	"""
	location = get_one_by_id(id, db)
	if not location:
		raise HTTPException(status_code=404, detail="Location does not exist")
	db.delete(location)
	db.commit()
	return location
		