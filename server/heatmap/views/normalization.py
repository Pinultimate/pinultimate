from math import *
import datetime
import time

def gridify(lat, lng, reso):
	LAT_SHIFT = 90
	LNG_SHIFT = 180
	lat_index = floor((lat + LAT_SHIFT) / reso)
	lng_index = floor((lng + LNG_SHIFT) / reso)
	#lat_index = floor((-lat + LAT_SHIFT) / reso)
	return lat_index, lng_index

def grid_center(lat_index, lng_index, reso):
	LAT_SHIFT = 90
	LNG_SHIFT = 180
	lat = (lat_index + 0.5) * reso - LAT_SHIFT
	lng = (lng_index + 0.5) * reso - LNG_SHIFT
	return lat, lng

def max_index(reso):
	return floor(180/reso), floor(360/reso)

def max_lat_index(reso):
	return floor(180/reso)

def max_lon_index(reso):
	return floor(360/reso)

def normalize_to_grid_center(lat, lng, reso):
	lat_index, lng_index = gridify(lat, lng, reso)
	return grid_center(lat_index, lng_index, reso)

def normalize_timestamp_to_hour(timestamp):
	return datetime.datetime(timestamp.year, timestamp.month, timestamp.day, timestamp.hour)