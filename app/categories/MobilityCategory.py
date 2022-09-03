from app.categories.Category import Category




class MobilityCategory(Category):
	client_mobility: int
	jober_mobility: int


	def __init__(self, weight: int, client_mobility: int, jober_mobility: int):
		self.weight = weight
		self.client_mobility = client_mobility
		self.jober_mobility = jober_mobility


	def compare(self):
		self.match_percentage = 100 if (self.client_mobility <= self.jober_mobility) else 0
		return self.match_percentage

	def to_dict(self):
		return {"mobility_category": self.match_percentage}