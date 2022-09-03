from sqlalchemy import Column, String, Integer, TIMESTAMP, text
from models.db import Base
from models.job.schemas import JobCreate, Job
from resources.data_preprocessing import preprocessing

class JobEntity(Base):
	__tablename__ = 'job'

	id = Column(Integer, primary_key=True, nullable=False, index=True)
	job_name = Column(String(100), nullable=False, unique=True)
	info = Column(String(350), nullable=True)
	cluster = Column(Integer, nullable=False, default=-1)
	created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
	updated_at = Column(
		TIMESTAMP,
		server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
	)


	def __init__(self, job_create: JobCreate):
		self.job_name = preprocessing(job_create.job_name, False).upper()


	def to_dict(self):
		return Job(
			id = self.id,
			job_name = self.job_name,
			info = self.info,
			cluster = self.cluster,
			created_at = self.created_at,
			updated_at = self.updated_at
		).dict()
