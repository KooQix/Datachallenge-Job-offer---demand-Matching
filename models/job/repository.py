from fastapi import HTTPException
from models.job.entity import JobEntity
from sqlalchemy.orm import Session
from models.db import Base, SessionLocal, engine
from models.job.schemas import JobCreate
import services.web.preprocessing as scrap_preprocessing
from resources.data_preprocessing import preprocessing

def get_all(db: Session):
	"""Get all jobs from the database

	Args:
		db (Session): Db Session

	Returns:
		List[JobEntity]: The list of jobs in the database
	"""
	return db.query(JobEntity).all()


def get_one_by_id(id: int, db: Session):
	"""Get job by id

	Args:
		id (int): Job id
		db (Session): Db Session

	Returns:
		JobEntity: The job
	"""
	return db.query(JobEntity).get(id)


def get_one_by_name(name: str, db: Session):
	"""Get job by name

	Args:
		name (str): Job name
		db (Session): Db Session

	Returns:
		JobEntity: The job where job name is name
	"""
	res: list[JobEntity] = db.query(JobEntity).all()
	for element in res:
		if (preprocessing(element.job_name, False) == preprocessing(name, False)):
			return element

	return None



def get_or_create(name: str):
	"""Create job if doesn't exist and return job where job_name == name

	Args:
		name (str): Job name

	Returns:
		JobEntity: Job where job_name == name
	"""
	Base.metadata.create_all(bind=engine)
	db: Session = SessionLocal()
	job = get_one_by_name(name, db)
	

	# Job doesn't exist yet, create it
	if (job == None):
		job_create = JobCreate(job_name = name)
		job = create(job_create, db)

	
	db.close()

	# Return job
	return job



def create(job_create: JobCreate, db: Session):
	"""Create a job entity

	Args:
		job_create (JobCreate): Job's information
		db (Session): Db Session

	Returns:
		JobEntity: Job created
	"""
	if (job_create.job_name == '' or job_create.job_name == None or str(job_create.job_name) == "nan"): return None
	data = scrap_preprocessing.preprocessing_data(job_create.job_name)
	if (data == None): return None
	job = JobEntity(job_create)

	data_splt = data.split(' ')
	job.info = ' '.join(data_splt[:10])
	db.add(job)
	db.commit()
	db.refresh(job)
	return job



def delete(id: int, db: Session):
	"""Delete a job

	Args:
		id (int): Job's id to delete
		db (Session): Db Session

	Raises:
		HTTPException: 

	Returns:
		JobEntity: The job that was deleted
	"""
	job = get_one_by_id(id, db)
	if not job:
		raise HTTPException(status_code=404, detail="Job does not exist")

	db.delete(job)
	db.commit()
	return job



def set_cluster(id: int, nb_cluster: int, db: Session):
	"""Set job cluster 

	Args:
		id (int): Job's id
		nb_cluster (int): cluster number of the job
		db (Session): Db Session

	Raises:
		HTTPException: 
	"""
	job = get_one_by_id(id, db)
	if not job:
		raise HTTPException(status_code=404, detail="Job does not exist")
	job.cluster = nb_cluster
	db.commit()
	db.refresh(job)



def get_cluster(id: int, db: Session):
	"""Get the job cluster number

	Args:
		id (int): Job's id
		db (Session): Db Session

	Raises:
		HTTPException: 

	Returns:
		int: The cluster number of the job
	"""
	job = get_one_by_id(id, db)
	if not job:
		raise HTTPException(status_code=404, detail="Job does not exist")

	return int(job.cluster)
	
	
def get_cluster(job_name: str, db: Session):
	"""Get the job cluster number

	Args:
		id (int): Job's id
		db (Session): Db Session

	Raises:
		HTTPException: 

	Returns:
		int: The cluster number of the job
	"""
	job = get_one_by_name(job_name, db)
	if not job:
		raise HTTPException(status_code=404, detail="Job does not exist")

	return int(job.cluster)