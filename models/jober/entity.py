from fastapi import HTTPException
from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, text, ForeignKey
from sqlalchemy.orm import relationship

from models.db import Base
from models.jober.schemas import JoberCreate, JoberUpdate

from models.job.entity import JobEntity
from models.job.repository import get_or_create as get_job_or_create
from models.location.repository import get_or_create

class JoberEntity(Base):
	__tablename__ = "jober"

	id = Column(Integer, primary_key=True, nullable=False, index=True)
	name = Column(String(100), nullable=False)
	surname = Column(String(100), nullable=False)
	zip_code = Column(Integer, nullable=False)
	city_id = Column(Integer, ForeignKey("location.id"), nullable=False)
	city = relationship("LocationEntity", foreign_keys=[city_id], lazy='subquery')
	last_job_id = Column(Integer, ForeignKey("job.id"), nullable=True)
	last_job = relationship("JobEntity", foreign_keys=[last_job_id], lazy='subquery')
	gender = Column(String(2), nullable=False)
	looking_for_job_id = Column(Integer, ForeignKey("job.id"), nullable=False)
	looking_for_job = relationship("JobEntity", foreign_keys=[looking_for_job_id], lazy='subquery')
	availability1 = Column(Integer, nullable=False)
	availability2 = Column(Integer, nullable=False)
	salary = Column(Integer, nullable=False)
	location_job = Column(String(100), nullable=False)
	company_size = Column(String(50), nullable=False)
	driver_license = Column(Boolean, nullable=False)
	tpe = Column(Boolean, nullable=False)
	pme = Column(Boolean, nullable=False)
	eti = Column(Boolean, nullable=False)
	big_company = Column(Boolean, nullable=False)
	skills1 = Column(String(100), nullable=False)
	skills2 = Column(String(100), nullable=False)
	skills3 = Column(String(100), nullable=False)
	contract_type1 = Column(String(100), nullable=False)
	contract_type2 = Column(String(100), nullable=False)
	contract_type3 = Column(String(100), nullable=False)
	contract_type_differences = Column(Boolean, nullable=False)
	if_not_more_info = Column(Boolean, nullable=False)
	teleworking = Column(Integer, nullable=False)
	max_distance = Column(Integer, nullable=False)
	ready_move_out = Column(Boolean, nullable=False)
	mobility = Column(Integer, nullable=False)
	created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
	updated_at = Column(
		TIMESTAMP,
		server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
	)



	def __init__(self, jober_create: JoberCreate):
		last_job: JobEntity = get_job_or_create(jober_create.last_job)
		looking_for_job: JobEntity = get_job_or_create(jober_create.looking_for_job)

		try:
			location = get_or_create(jober_create.city)
		except Exception as e:
			raise Exception(f"Invalid location: {jober_create.city}")
		

		self.name = jober_create.name
		self.surname = jober_create.surname
		self.zip_code = jober_create.zip_code
		self.city_id = location.id
		self.last_job_id = last_job.id if (last_job != None) else None
		self.gender = jober_create.gender
		self.looking_for_job_id = looking_for_job.id if(looking_for_job != None) else None
		self.availability1 = jober_create.availability1
		self.availability2 = jober_create.availability2
		self.salary = jober_create.salary
		self.location_job = jober_create.location_job
		self.company_size = jober_create.company_size
		self.driver_license = jober_create.driver_license
		self.tpe = jober_create.tpe
		self.pme = jober_create.pme
		self.eti = jober_create.eti
		self.big_company = jober_create.big_company
		self.skills1 = jober_create.skills1
		self.skills2 = jober_create.skills2
		self.skills3 = jober_create.skills3
		self.contract_type1 = jober_create.contract_type1
		self.contract_type2 = jober_create.contract_type2
		self.contract_type3 = jober_create.contract_type3
		self.contract_type_differences = jober_create.contract_type_differences
		self.if_not_more_info = jober_create.if_not_more_info
		self.teleworking = jober_create.teleworking
		self.max_distance = jober_create.max_distance
		self.ready_move_out = jober_create.ready_move_out
		self.mobility = jober_create.mobility
  
  
  
	def update(self, jober_update: JoberUpdate):
		
		self.name = jober_update.name or self.name
		self.surname = jober_update.surname or self.surname
		self.zip_code = jober_update.zip_code or self.zip_code

		try:
			self.city_id = get_or_create(jober_update.city).id if (jober_update.city != None and jober_update.city != '') else self.city_id
		except Exception as e:
			raise Exception(f"Invalid location: {jober_update.city}")

		self.last_job_id = get_job_or_create(jober_update.last_job).id if (jober_update.last_job != None and jober_update.last_job != "" ) else self.last_job_id
		self.gender = jober_update.gender or self.gender
		self.looking_for_job_id = get_job_or_create(jober_update.looking_for_job).id if (jober_update.looking_for_job != "" and jober_update.looking_for_job != None) else self.looking_for_job_id
		self.availability1 = jober_update.availability1 or self.availability1
		self.availability2 = jober_update.availability2 or self.availability2
		self.salary = jober_update.salary or self.salary
		self.location_job = jober_update.location_job or self.location_job
		self.company_size = jober_update.company_size or self.company_size
		self.driver_license = jober_update.driver_license or self.driver_license
		self.tpe = jober_update.tpe or self.tpe
		self.pme = jober_update.pme or self.pme
		self.eti = jober_update.eti or self.eti
		self.big_company = jober_update.big_company or self.big_company
		self.skills1 = jober_update.skills1 or self.skills1
		self.skills2 = jober_update.skills2 or self.skills2
		self.skills3 = jober_update.skills3 or self.skills3
		self.contract_type1 = jober_update.contract_type1 or self.contract_type1
		self.contract_type2 = jober_update.contract_type2 or self.contract_type2
		self.contract_type3 = jober_update.contract_type3 or self.contract_type3
		self.contract_type_differences = jober_update.contract_type_differences or self.contract_type_differences
		self.if_not_more_info = jober_update.if_not_more_info or self.if_not_more_info
		self.teleworking = jober_update.teleworking or self.teleworking
		self.max_distance = jober_update.max_distance or self.max_distance
		self.ready_move_out = jober_update.ready_move_out or self.ready_move_out
		self.mobility = jober_update.mobility or self.mobility
		return self
  

    

	