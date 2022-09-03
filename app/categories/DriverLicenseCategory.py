from app.categories.Category import Category



class DriverLicenseCategory(Category):
	driver_license_client: bool
	driver_license_jober: bool


	def __init__(self, 
			weight: int, 
			driver_license_client: bool, 
			driver_license_jober: bool
		):
		self.weight = weight
		self.driver_license_client = driver_license_client
		self.driver_license_jober = driver_license_jober

	def compare(self):
		self.match_percentage = 100 if (self.driver_license_client == self.driver_license_jober) else 0
		return self.match_percentage


	def to_dict(self):
		return {"driver_license_category": self.match_percentage}



	