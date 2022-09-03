
from resources.data_preprocessing import preprocessing
from models.job.schemas import Job
from models.jober.schemas import Jober


class Jober:

	#################### Jober categories to match with client's ####################
	
	last_job: Job
	looking_for_job: Job

	availability: int

	salary: int

	driver_license: bool

	skills: str

	teleworking: int

	city: str
	max_distance: int
	ready_move_out: bool

	mobility: int

	tpe: bool
	pme: bool
	eti: bool
	big_company: bool




	def __init__(self, jober: Jober):
		self.city = jober.city
		self.last_job = jober.last_job
		self.looking_for_job = jober.looking_for_job
		self.availability = max(jober.availability1, jober.availability2)
		self.salary = jober.salary
		self.driver_license = jober.driver_license
		self.skills = preprocessing(f"{jober.skills1} {jober.skills2} {jober.skills3}", True)
		self.teleworking = jober.teleworking
		self.max_distance = jober.max_distance
		self.ready_move_out = jober.ready_move_out
		self.mobility = jober.mobility
		self.tpe = jober.tpe
		self.pme = jober.pme
		self.eti = jober.eti
		self.big_company = jober.big_company
