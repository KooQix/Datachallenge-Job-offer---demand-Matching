from app.categories.Category import Category
from models.client.CompanySize import CompanySize



class CompanySizeCategory(Category):
	company_size_client: CompanySize

	jober_tpe: bool
	jober_pme: bool
	jober_eti: bool
	jober_big_company: bool

	step_increaser = 0.8

	def __init__(self, 
			weight: int, 
			company_size_client: CompanySize, 
			jober_tpe: bool, 
			jober_pme: bool, 
			jober_eti: bool, 
			jober_big_company: bool
		):
		self.weight = weight
		self.company_size_client = company_size_client
		self.jober_tpe = jober_tpe
		self.jober_pme = jober_pme
		self.jober_eti = jober_eti
		self.jober_big_company = jober_big_company


	def compare(self):
		self.match_percentage = max(
			[
				self.percentage_tpe(), 
				self.percentage_pme(), 
				self.percentage_eti(), 
				self.percentage_big_company()
			]
		)
		return self.match_percentage
		

	def get_percentage(self, company_size_client: CompanySize, company_size_jober: CompanySize):
		_max = max(company_size_client, company_size_jober)
		_min = min(company_size_client, company_size_jober)
		# "distance" in %
		percentage = (_max - _min) * 100 / (_max)
		# percentage match = 100 - distance in %
		return int(100 - (self.step_increaser * percentage))



	def percentage_tpe(self):
		if (not(self.jober_tpe)): return 0

		return self.get_percentage(CompanySize.TPE, self.company_size_client)
		


	def percentage_pme(self):
		if (not(self.jober_pme)): return 0

		return self.get_percentage(CompanySize.PME, self.company_size_client)



	def percentage_eti(self):
		if (not(self.jober_eti)): return 0

		return self.get_percentage(CompanySize.ETI, self.company_size_client)



	def percentage_big_company(self):
		if (not(self.jober_big_company)): return 0

		return self.get_percentage(CompanySize.BIG_COMPANY, self.company_size_client)


	def to_dict(self):
		return {"company_size_category": self.match_percentage}




	
