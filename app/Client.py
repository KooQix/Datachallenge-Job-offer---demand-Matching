from models.job.schemas import Job
from resources.data_preprocessing import preprocessing
from models.client.CompanySize import CompanySize
from models.client.schemas import Client

class Client:
	
	
	#################### Client categories to match with jober's ####################
	
	worktime: int
	salary: int
	city: str
	driver_license: bool
	company_size: CompanySize
	skills: str
	teleworking: int
	mobility: int
	job: Job


	def __init__(self, client: Client):
		self.worktime = client.worktime
		self.salary = client.salary
		self.city = client.location
		self.driver_license = client.driver_license
		self.company_size = client.company_size
		self.skills = preprocessing(f"{client.skills1} {client.skills2} {client.skills3}", True)
		self.teleworking = client.teleworking
		self.mobility = client.travel
		self.job = client.job_name

