from app.categories.Category import Category
from resources.data_preprocessing import preprocessing



class SkillsCategory(Category):
	skills_client: str
	skills_jober: str


	def __init__(self, weight: int, skills_client: str, skills_jober: str):
		self.weight = weight
		
		# Skills already concatenated and preprocessed
		self.skills_client = skills_client
		self.skills_jober = skills_jober

	

	def compare(self):
		skills_client_split = self.skills_client.split(' ')
		skills_jober_split = self.skills_jober.split(' ')

		match_client = 0
		for skill in skills_client_split:
			if (skill in skills_jober_split):
				match_client += 1

		match_jober = 0
		for skill in skills_jober_split:
			if (skill in skills_client_split):
				match_jober += 1

		self.match_percentage = int((match_client + match_jober) * 100 / (len(skills_jober_split) + len(skills_client_split)))
		return self.match_percentage


	def to_dict(self):
		return {"skills_category": self.match_percentage}