from math import *
import datetime
import time

def gridify(lat, lng, reso):
	LAT_SHIFT = 90
	LNG_SHIFT = 180
	lat_index = floor((lat + LAT_SHIFT) / reso)
	lng_index = floor((lng + LNG_SHIFT) / reso)
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

def normalize_timestamp_to_minute(timestamp):
	return datetime.datetime(timestamp.year, timestamp.month, timestamp.day, timestamp.hour, timestamp.minute)

def convert_to_bottom_left(lon, lat, lonrange, latrange):
	bottom_left_lon = lon - lonrange/2
	if bottom_left_lon < -180:
		bottom_left_lon = 180-(-180-bottom_left_lon)

	bottom_left_lat = lat - latrange/2
	if bottom_left_lat < -90:
		buttom_left_lat = 90-(-90-bottom_left_lat)

	return bottom_left_lon, bottom_left_lat

def convert_to_upper_right(lon, lat, lonrange, latrange):
	upper_right_lon = lon + lonrange/2
	if upper_right_lon > 180:
		upper_right_lon = -180+(upper_right_lon-180)

	upper_right_lat = lat + latrange/2
	if upper_right_lat > 90:
		upper_right_lat = -90+(upper_right_lat-90)
		
	return upper_right_lon, upper_right_lat