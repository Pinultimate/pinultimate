from math import *

def gridify(lat, lng, reso):
	LAT_SHIFT = 90
	LNG_SHIFT = 180
	lng_index = math.floor((lng + LNG_SHIFT) / reso)
	lat_index = math.floor((-lat + LAT_SHIFT) / reso)
	return lat_index, lng_index

def grid_center(lat_index, lng_index, reso):
	LAT_SHIFT = 90
	LNG_SHIFT = 180
	lat = -(lat_index + 0.5) * reso + LAT_SHIFT
	lng = (lng_index + 0.5) * reso - LNG_SHIFT
	return lat, lng

def max_index(reso):
	return math.floor(180/reso), math.floor(360/reso)

def normalize_to_grid_center(lat, lng, reso):
	lat_index, lng_index = gridify(lat, lng, reso)
	return grid_center(lat_index, lng_index, reso)