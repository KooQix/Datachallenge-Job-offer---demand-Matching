
from app.Client import Client as ClientMatch
from app.Jober import Jober as JoberMatch
from app.categories.CompanySizeCategory import CompanySizeCategory
from app.categories.DriverLicenseCategory import DriverLicenseCategory
from app.categories.JobQualitiesCategory import JobQualitiesCategory
from app.categories.MatchPercentageCategory import MatchPercentageCategory
from app.categories.MobilityCategory import MobilityCategory
from app.categories.SkillsCategory import SkillsCategory

from models.client.schemas import Client
from models.jober.schemas import Jober

from os import environ
class Match:
	match_percentage: int
	
	
	#################### Categories ####################

	job_qualities: JobQualitiesCategory
	skills: SkillsCategory
	worktime: MatchPercentageCategory
	teleworking: MatchPercentageCategory
	salary: MatchPercentageCategory
	driver_license: DriverLicenseCategory
	mobility: MobilityCategory
	company_size: CompanySizeCategory

	#################### Categories Weights ####################

	WEIGHT_JOB_QUALITIES = float(environ.get('WEIGHT_JOB_QUALITIES'))
	WEIGHT_SKILLS = float(environ.get('WEIGHT_SKILLS'))
	WEIGHT_WORKTIME = float(environ.get('WEIGHT_WORKTIME'))
	WEIGHT_TELEWORKING = float(environ.get('WEIGHT_TELEWORKING'))
	WEIGHT_SALARY = float(environ.get('WEIGHT_SALARY'))
	WEIGHT_DRIVER_LICENSE = float(environ.get('WEIGHT_DRIVER_LICENSE'))
	WEIGHT_MOBILITY = float(environ.get('WEIGHT_MOBILITY'))
	WEIGHT_COMPANY_SIZE = float(environ.get('WEIGHT_COMPANY_SIZE'))


	def __init__(self, _jober: Jober, _client: Client, clusters_centroids: list[list[float]]):
		jober = JoberMatch(_jober)
		client = ClientMatch(_client)
		self.job_qualities = JobQualitiesCategory(self.WEIGHT_JOB_QUALITIES, clusters_centroids, client.job, jober.last_job, jober.looking_for_job)

		self.skills = SkillsCategory(self.WEIGHT_SKILLS, client.skills, jober.skills)

		self.worktime = MatchPercentageCategory(self.WEIGHT_WORKTIME, "worktime", client.worktime, jober.availability)

		self.teleworking =  MatchPercentageCategory(self.WEIGHT_TELEWORKING, "teleworking", client.teleworking, jober.teleworking)

		self.salary = MatchPercentageCategory(self.WEIGHT_SALARY, "salary", client.salary, jober.salary, step_increaser=0.95)

		self.driver_license = DriverLicenseCategory(self.WEIGHT_DRIVER_LICENSE, client.driver_license, jober.driver_license)

		self.mobility = MobilityCategory(self.WEIGHT_MOBILITY, client.mobility, jober.mobility)

		self.company_size = CompanySizeCategory(self.WEIGHT_COMPANY_SIZE, client.company_size, jober.tpe, jober.pme, jober.eti, jober.big_company)

	


	def get_match_percentage(self):
		match_percentage = 0

		# Compare each category and weight the percentage of each
		match_percentage += self.job_qualities.compare() * self.job_qualities.weight

		match_percentage += self.skills.compare() * self.skills.weight

		match_percentage += self.worktime.compare() * self.worktime.weight

		match_percentage += self.teleworking.compare() * self.teleworking.weight

		match_percentage += self.salary.compare() * self.salary.weight

		match_percentage += self.driver_license.compare() * self.driver_license.weight

		match_percentage += self.mobility.compare() * self.mobility.weight

		match_percentage += self.company_size.compare() * self.company_size.weight

		self.match_percentage = match_percentage
		return self.match_percentage

	
	def get_info(self):
		info: list[dict[str, int]] = []
		
		info.append(self.job_qualities.to_dict())
		info.append(self.skills.to_dict())
		info.append(self.worktime.to_dict())
		info.append(self.teleworking.to_dict())
		info.append(self.salary.to_dict())
		info.append(self.driver_license.to_dict())
		info.append(self.mobility.to_dict())
		info.append(self.company_size.to_dict())
		
		return info