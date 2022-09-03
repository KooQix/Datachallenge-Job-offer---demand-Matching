from fastapi import HTTPException
from models.client.entity import ClientEntity
from models.client.schemas import *
from sqlalchemy.orm import Session


        


def get_all(db: Session):
	"""Get all clients

	Args:
		db (Session): Db session

	Returns:
		List[ClientEntity]: The list of clients in database
	"""
	return db.query(ClientEntity).all()


def get_one_by_id(id: int, db: Session):
	"""Get client by id

	Args:
		db (Session): Db session
		id (int): Client id

	Returns:
		ClientEntity: The client 
	"""
	return db.query(ClientEntity).get(id)



def create(client_create: ClientCreate, db: Session):
	"""Create client

	Args:
		db (Session): Db Session
		client_create (ClientCreate): Client's information

	Returns:
		ClientEntity: Client created
	"""
	client = ClientEntity(client_create)
	db.add(client)
	db.commit()
	db.refresh(client)
	return client



def update(id: int, client_update: ClientUpdate, db: Session):
	"""Update a client entity

	Args:
		id (int); Client's id
		client_update (ClientUpdate): Client's information to update
		db (Session): DB Session

	Raises:
		HTTPException: 

	Returns:
		ClientEntity: The client updated
	"""
	client: ClientEntity = get_one_by_id(id, db)
	if not client:
		raise HTTPException(status_code=404, detail="Client does not exist")

	client: ClientEntity = client.update(client_update)
	db.commit()
	db.refresh(client)
	return client

 
 
def delete(id: int, db: Session):
	"""Delete a client

	Args:
		id (int): The id of the client to delete
		db (Session): Db Session

	Raises:
		HTTPException: 

	Returns:
		ClientEntity: The client that was deleted
	"""
	client = get_one_by_id(id, db)
	if not client:
		raise HTTPException(status_code=404, detail="Client does not exist")

	db.delete(client)
	db.commit()
	return client