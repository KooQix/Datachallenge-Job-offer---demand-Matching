from pydantic import BaseModel
from datetime import date




class LocationCreate(BaseModel):
	city: str
	country: str

	class Config:
		orm_mode = True


class Location(LocationCreate):
	id: int
	latitude: float
	longitude: float
	created_at: date
	updated_at: date

	class Config:
		orm_mode = True

	