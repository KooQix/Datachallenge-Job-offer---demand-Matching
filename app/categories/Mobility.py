


from models.location.entity import LocationEntity


class Mobility():
	city_client: LocationEntity
	city_jober: LocationEntity

	max_distance_jober: int
	ready_move_out: bool

	def __init__(self, city_client: LocationEntity, city_jober: LocationEntity, max_distance_jober: int, ready_move_out: bool):
		self.city_client = city_client
		self.city_jober = city_jober
		self.max_distance_jober = max_distance_jober
		self.ready_move_out = ready_move_out

	
	def compare(self):
		"""Whether the client and jober are within distance

		Returns:
			bool: Whether the client and jober are within distance
		"""
		if (not(self.city_client.is_valid()) or not(self.city_jober.is_valid())): return False

		if (self.ready_move_out): return True

		distance = self.city_client.distance_to(self.city_jober)
		return bool(distance != None and distance <= self.max_distance_jober)
		
	

