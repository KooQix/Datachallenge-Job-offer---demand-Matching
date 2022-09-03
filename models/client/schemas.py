from typing import Optional
from pydantic import BaseModel
from datetime import date
from models.job.schemas import Job
from models.location.schemas import Location

class ClientBase(BaseModel):
	multi: bool
	contract_type: str
	contract_type_differences: str
	if_not_more_info: str
	worktime: int
	salary: int
	location: str
	driver_license: bool
	company_size: int
	other_license: bool
	skills1: str
	skills2: str
	skills3: str
	teleworking: int
	travel: int
	required_resume: bool
	name: str
	surname: str
	company_name: str
	hq_location: str
	siret: str
	naf: str
 
	class Config:
		orm_mode = True


class ClientCreate(ClientBase):
    
	job_name: str
	class Config:
		orm_mode = True
  
  
class Client(ClientBase):
    
	id: int
	location: Location
	job_name: Job
	created_at: date
	updated_at: date
 
	class Config:
		orm_mode = True



class ClientUpdate(BaseModel):
    
	job_name: Optional[str]
	multi: Optional[bool]
	contract_type: Optional[str]
	contract_type_differences: Optional[str]
	if_not_more_info: Optional[str]
	worktime: Optional[int]
	salary: Optional[int]
	location: Optional[str]
	driver_license: Optional[int]
	company_size: Optional[int]
	other_license: Optional[bool]
	skills1: Optional[str]
	skills2: Optional[str]
	skills3: Optional[str]
	teleworking: Optional[int]
	travel: Optional[int]
	required_resume: Optional[bool]
	name: Optional[str]
	surname: Optional[str]
	company_name: Optional[str]
	hq_location: Optional[str]
	siret: Optional[str]
	naf: Optional[str]
	class Config:
		orm_mode = True



class ClientMatch(ClientCreate):
	id: int
	match_percentage: int
	match_info: list[dict[str, int]]
