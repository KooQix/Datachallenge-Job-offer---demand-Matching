from sqlalchemy import Boolean, Column, String, Integer, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship
from models.client.schemas import ClientCreate, ClientUpdate
from models.job.entity import JobEntity
from models.job.repository import get_or_create as get_job_or_create
from models.db import Base
from models.location.repository import get_or_create


class ClientEntity(Base):
	__tablename__ = "client"

	id = Column(Integer, primary_key=True, nullable=False, index=True)
	job_name_id = Column(Integer, ForeignKey("job.id"), nullable=True)
	job_name = relationship("JobEntity", foreign_keys=[job_name_id], lazy='subquery')
	multi = Column(Boolean, nullable=False)
	contract_type = Column(String(255), nullable=False)
	contract_type_differences = Column(String(255), nullable=False)
	if_not_more_info = Column(String(50), nullable=False)
	worktime = Column(Integer, nullable=False)
	salary = Column(Integer, nullable=False)
	location_id = Column(Integer, ForeignKey("location.id"), nullable=False)
	location = relationship("LocationEntity", foreign_keys=[location_id], lazy='subquery')
	driver_license = Column(Integer, nullable=False)
	company_size = Column(Integer, nullable=False)
	other_license = Column(Boolean, nullable=False)
	skills1 = Column(String(255), nullable=False)
	skills2 = Column(String(255), nullable=False)
	skills3 = Column(String(255), nullable=False)
	teleworking = Column(Integer, nullable=False)
	travel = Column(Integer, nullable=False)
	required_resume = Column(Boolean, nullable=False)
	name = Column(String(100), nullable=False)
	surname = Column(String(100), nullable=False)
	company_name = Column(String(100), nullable=False)
	hq_location = Column(String(100), nullable=False)
	siret = Column(String(100), nullable=False)
	naf = Column(String(20), nullable=False)
	created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
	updated_at = Column(
		TIMESTAMP,
		server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
	)


	def __init__(self, client_create: ClientCreate):
		job: JobEntity = get_job_or_create(client_create.job_name)

		try:
			location = get_or_create(client_create.location)
		except Exception as e:
			raise Exception(f"Invalid location: {client_create.location}")
		

		self.job_name_id = job.id if (job != None) else None
		self.multi = client_create.multi
		self.contract_type = client_create.contract_type
		self.contract_type_differences = client_create.contract_type_differences
		self.if_not_more_info = client_create.if_not_more_info
		self.worktime = client_create.worktime
		self.salary = client_create.salary
		self.location_id = location.id
		self.driver_license = client_create.driver_license
		self.company_size = client_create.company_size
		self.other_license = client_create.other_license
		self.skills1 = client_create.skills1
		self.skills2 = client_create.skills2
		self.skills3 = client_create.skills3
		self.teleworking = client_create.teleworking
		self.travel = client_create.travel
		self.required_resume = client_create.required_resume
		self.name = client_create.name
		self.surname = client_create.surname
		self.company_name = client_create.company_name
		self.hq_location = client_create.hq_location
		self.siret = client_create.siret
		self.naf = client_create.naf
  
  

	def update(self, client_update: ClientUpdate):

		self.job_name_id = get_job_or_create(client_update.job_name).id if(client_update.job_name != None and client_update.job_name != "") else self.job_name_id
		self.multi = client_update.multi or self.multi
		self.contract_type = client_update.contract_type or self.contract_type
		self.contract_type_differences = client_update.contract_type_differences or self.contract_type_differences
		self.if_not_more_info = client_update.if_not_more_info or self.if_not_more_info
		self.worktime = client_update.worktime or self.worktime
		self.salary = client_update.salary or self.salary

		
		try:
			self.location_id = get_or_create(client_update.location).id if (client_update.location != None and client_update.location != '') else self.location_id
		except Exception as e:
			raise Exception(f"Invalid location: {client_update.location}")

		self.driver_license = client_update.driver_license or self.driver_license
		self.company_size = client_update.company_size or self.company_size
		self.other_license = client_update.other_license or self.other_license
		self.skills1 = client_update.skills1 or self.skills1
		self.skills2 = client_update.skills2 or self.skills2
		self.skills3 = client_update.skills3 or self.skills3
		self.teleworking = client_update.teleworking or self.teleworking
		self.travel = client_update.travel or self.travel
		self.required_resume = client_update.required_resume or self.required_resume
		self.name = client_update.name or self.name
		self.surname = client_update.surname or self.surname
		self.company_name = client_update.company_name or self.company_name
		self.hq_location = client_update.hq_location or self.hq_location
		self.siret = client_update.siret or self.siret
		self.naf = client_update.naf or self.naf
		return self