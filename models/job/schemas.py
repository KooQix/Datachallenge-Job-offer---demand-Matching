from pydantic import BaseModel
from datetime import date





class JobCreate(BaseModel):
	job_name: str

	class Config:
		orm_mode = True


class Job(JobCreate):
	id: int
	info: str
	cluster: int
	created_at: date
	updated_at: date

	class Config:
		orm_mode = True




 
	
 
