import os
import sys
import json
import math


class Grid_mapping:

	def __init__(self):
		self.LAT_SHIFT = 90
		self.LNG_SHIFT = 180

	def gridify(self, lat, lng reso):
		lng_index = math.floor((lng + self.LNG_SHIFT) / reso)
		lat_index = math.floor((-lat + self.LAT_SHIFT) / reso)
		return lat_index, lng_index

	def grid_center(self, lat_index, lng_index, reso):
		lat = -(lat_index + 0.5) * reso + self.LAT_SHIFT
		lng = (lng_index + 0.5) * reso - self.LNG_SHIFT
		center = {'longitude': lng, 'latitude': lat}
		return center

	def max_index(self, reso):
		return math.floor(180/reso), math.floor(360/reso)


