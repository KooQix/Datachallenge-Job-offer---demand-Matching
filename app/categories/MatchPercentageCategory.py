from app.categories.Category import Category



class MatchPercentageCategory(Category):
	percentage_1: int
	percentage_2: int

	step_increaser: float
	category_name: str

	def __init__(self, weight: int, category_name: str, percentage_1: int, percentage_2: int, step_increaser = 1):
		self.weight = weight
		self.category_name = category_name
		self.percentage_1 = percentage_1
		self.percentage_2 = percentage_2

		if (step_increaser < 1 and step_increaser > 0):
			self.step_increaser = step_increaser

		else:
			self.step_increaser = 1

	
	def compare(self):
		_max = max(self.percentage_1, self.percentage_2)
		_min = min(self.percentage_1, self.percentage_2)
		# "distance" in %
		percentage = (_max - _min) * 100 / (_max)
		# percentage match = 100 - distance in %
		self.match_percentage = int(100 - (self.step_increaser * percentage))
		return self.match_percentage


	def to_dict(self):
		return {f"{self.category_name}_category": self.match_percentage}

