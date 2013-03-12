from django.http import HttpResponse
from heatmap.models import *
from collections import OrderedDict
import json
import datetime
import time
from math import *

def normalize_timestamp(timestamp):
	# TODO: handle tzinfo if necessary in the future
	return datetime.datetime(timestamp.year, timestamp.month, timestamp.day, timestamp.hour)

# if a specific timestamp (1-hour-interval) has zero checkins, then that key-value pair is not included in the json
# radious: in degrees
# timestamps is a list
def query_radius(lat=None, lon=None, rad=None, timestamps=None):
	response = OrderedDict()
	locations = Location.objects
	for location in locations:
		n_timestamp = normalize_timestamp(location.timestamp)
		if timestamps is not None:
			if n_timestamp not in timestamps:
				continue

		if (rad is not None) and (lat is not None) and (lon is not None):
			dist = sqrt(pow(location.coordinates[0] - lat, 2) + pow(location.coordinates[1] - lon, 2))
			if dist > rad:
				continue

		n_timestamp_str = n_timestamp.strftime('%Y-%m-%d %H:%M:%S')
		if n_timestamp_str not in response:
			response[n_timestamp_str] = []
		response[n_timestamp_str].append(location.coordinates)
	return response

def query_region(lat=None, lon=None, latrange=None, lonrange=None, timestamps=None):
	response = OrderedDict()
	locations = Location.objects
	for location in locations:
		n_timestamp = normalize_timestamp(location.timestamp)
		if timestamps is not None:
			if n_timestamp not in timestamps:
				continue

		if (lat is not None) and (lon is not None):
			if (latrange is not None):
				if (location.coordinates[0] > lat + latrange/2) or (location.coordinates[0] < lat - latrange/2):
					continue
			if (lonrange is not None):
				if (location.coordinates[1] > lon + lonrange/2) or (location.coordinates[1] < lon - lonrange/2):
					continue

		n_timestamp_str = n_timestamp.strftime('%Y-%m-%d %H:%M:%S')
		if n_timestamp_str not in response:
			response[n_timestamp_str] = []
		response[n_timestamp_str].append(location.coordinates)
	return response

def search(request, lat=None, lon=None, rad=None, latrange=None, lonrange=None, year=None, month=None, day=None, hour=None, minute=None, type=None):
	
	if (year is not None) and (month is not None) and (day is not None):
		timestamps = []
		if minute is not None:
			timestamp = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute))
			timestamps.append(normalize_timestamp(timestamp))
		else:
			if hour is not None:
				timestamp = datetime.datetime(int(year), int(month), int(day), int(hour))
				timestamps.append(normalize_timestamp(timestamp))
			else:
				for hour in range(24):
					timestamp = datetime.datetime(int(year), int(month), int(day), hour)
					timestamps.append(normalize_timestamp(timestamp))
	else:
		timestamps = None

	if (type is None):
		response = query_radius(timestamps=timestamps)
	elif (type is 'reg'):
		response = query_region(float(lat), float(lon), float(latrange), float(lonrange), timestamps)
	elif (type is 'rad'):
		response = query_radius(float(lat), float(lon), float(rad), timestamps)
	else:
		print 'Error: Incorrect type: %s passed to query URL...' % type
	return HttpResponse(json.dumps(response), content_type="application/json")

'''
def add_location_now(request, latitude, longitude):
	location = Location(
		coordinates=[float(latitude), float(longitude)],
		timestamp=datetime.datetime.now(),
	)
	location.save()
	return HttpResponse('Added %s' % location.coordinates)
'''
