from typing import Optional
from pydantic import BaseModel
from datetime import date
from models.job.schemas import Job

from models.location.schemas import Location


class JoberCreate(BaseModel):
    
	name: str
	surname: str
	zip_code: int
	city: str
	last_job: str
	gender: str
	looking_for_job: str
	availability1: int
	availability2: int
	salary: int
	location_job: str
	company_size: str
	driver_license: bool
	tpe: bool
	pme: bool
	eti: bool
	big_company: bool
	skills1: str
	skills2: str
	skills3: str
	contract_type1: str
	contract_type2: str
	contract_type3: str
	contract_type_differences: bool
	if_not_more_info: bool
	teleworking: int
	max_distance: int
	ready_move_out: bool
	mobility: int
	class Config:
		orm_mode = True
  
  
class Jober(JoberCreate):
    
	id: int
	city: Location
	last_job: Optional[Job]
	looking_for_job: Job
	created_at: date
	updated_at: date

	class Config:
		orm_mode = True
  
  
class JoberUpdate(BaseModel):
    
	name: Optional[str]
	surname: Optional[str]
	zip_code: Optional[int]
	city: Optional[str]
	last_job: Optional[str]
	gender: Optional[str]
	looking_for_job: Optional[str]
	availability1: Optional[int]
	availability2: Optional[int]
	salary: Optional[int]
	location_job: Optional[str]
	company_size: Optional[str]
	driver_license: Optional[bool]
	tpe: Optional[bool]
	pme: Optional[bool]
	eti: Optional[bool]
	big_company: Optional[bool]
	skills1: Optional[str]
	skills2: Optional[str]
	skills3: Optional[str]
	contract_type1: Optional[str]
	contract_type2: Optional[str]
	contract_type3: Optional[str]
	contract_type_differences: Optional[bool]
	if_not_more_info: Optional[bool]
	teleworking: Optional[int]
	max_distance: Optional[int]
	ready_move_out: Optional[bool]
	mobility: Optional[int]
	class Config:
		orm_mode = True



class JoberMatch(JoberCreate):
	id: int
	match_percentage: int
	match_info: list[dict[str, int]]
