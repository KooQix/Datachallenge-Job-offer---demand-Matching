

from abc import abstractmethod


class Category:
	weight: int
	match_percentage: int

	@abstractmethod
	def compare(self):
		"""Get the percentage of match for this category

		Returns:
			int: Return the percentage of match
		"""
		pass

	@abstractmethod
	def to_dict(self):
		"""Return the category name, match percentage as a dict
		"""
		pass

