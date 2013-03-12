from django.http import HttpResponse
from heatmap.models import *
from collections import OrderedDict
import json
import datetime
import time

def normalize_timestamp(timestamp):
	# TODO: handle tzinfo if necessary in the future
	return datetime.datetime(timestamp.year, timestamp.month, timestamp.day, timestamp.hour)

# if a specific timestamp (1-hour-interval) has zero checkins, then that key-value pair is not included in the json
# radious: in degrees
# timestamps is a list
def query(lat=None, lon=None, rad=None, timestamps=None):
	response = OrderedDict()
	locations = Location.objects
	for location in locations:
		n_timestamp = normalize_timestamp(location.timestamp)
		if timestamps is not None:
			if n_timestamp not in timestamps:
				continue

		if (rad is not None) and (lat is not None) and (lon is not None):
			if (location.coordinates[0] > lat + rad) or (location.coordinates[0] < lat - rad):
				continue
			if (location.coordinates[1] > lon + rad) or (location.coordinates[1] < lon - rad):
				continue

		n_timestamp_str = n_timestamp.strftime('%Y-%m-%d %H:%M:%S')
		if n_timestamp_str not in response:
			response[n_timestamp_str] = []
		response[n_timestamp_str].append(location.coordinates)
	return response

def search(request, lat=None, lon=None, rad=None, year=None, month=None, day=None, hour=None, minute=None):
	if (lat is not None) and (lon is not None) and (rad is not None):
		lat = float(lat)
		lon = float(lon)
		rad = float(rad)
	else:
		lat = None
		lon = None
		rad = None
	
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

	response = query(lat, lon, rad, timestamps)
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
