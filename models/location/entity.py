from typing_extensions import Self
from fastapi import HTTPException
from sqlalchemy import Column, String, Integer, TIMESTAMP, text, Float
from models.db import Base
import math
from geopy.geocoders import Nominatim


class LocationEntity(Base):
	__tablename__ = 'location'

	id = Column(Integer, primary_key=True, nullable=False, index=True)
	city = Column(String(255), nullable=False, unique=True)
	country = Column(String(255), nullable=False, default="France")
	latitude = Column(Float, nullable=False)
	longitude = Column(Float, nullable=False)
	created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
	updated_at = Column(
		TIMESTAMP,
		server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
	)


	def __init__(self, city: str, country: str = "France"):
		self.city = city
		self.country = country
		self.get_coordinates()


	def is_valid(self):
		"""Valid if the coordinates have successfully been retrieved

		Returns:
			bool: False if latitude == None or longitude == None
		"""
		return self.latitude != None and self.longitude != None



	def get_coordinates(self):
		"""Get the coordinates of the given city
		"""
		geolocator = Nominatim(user_agent="http")
		address = geolocator.geocode(f"{self.city},{self.country}")
		self.latitude = address.latitude if (address != None) else None
		self.longitude = address.longitude if (address != None) else None

	def distance_to(self, other_location: Self):
		"""Return the distance (km) between city and other_city

		Args:
			other_city (Self): The other city 

		Returns:
			int: The distance (km) between city and other_city
		"""
		if not(other_location.is_valid()): return None

		R = 6371 # km
		lat_dist = math.radians(self.latitude - other_location.latitude)
		long_dist = math.radians(self.longitude - other_location.longitude)
		
		sin_lat = math.sin(lat_dist/2)
		sin_long = math.sin(long_dist/2)

		a = sin_lat * sin_lat + (math.cos(math.radians(self.latitude)) *
            math.cos(math.radians(other_location.latitude)) *
            sin_long * sin_long)

		c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
		return int(R * c)