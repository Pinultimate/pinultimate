from django.http import HttpResponse
from heatmap.models import *
from collections import defaultdict
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
	response = defaultdict(list)
	locations = Location.objects
	i = 1
	for location in locations:
		n_timestamp = normalize_timestamp(location.timestamp)		
		if timestamp is not None:
			if n_timestamp not in timestamps:
				continue

		if (rad is not None) and (lat is not None) and (lon is not None):
			# geo spatial search true / false
			if (location.coordinates.latitude > lat + rad) or (location.coordinates.latitude > lat - rad):
				continue
			if (location.coordinates.longitude > lon + rad) or (location.coordinates.longitude > lon - rad):
				continue

		n_timestamp_str = n_timestamp.strftime('%Y-%m-%d %H:%M:%S')
		response[n_timestamp_str].append(location.coordinates)
	return response

'''
def search(request):
	response = query()
	return HttpResponse(json.dumps(response), content_type="application/json")

def search_radius(request, lat, lon, radius):
	response = query(lat=float(lat), lon=float(lon), radius=float(radius))
	return HttpResponse(json.dumps(response), content_type="application/json")

# Create your views here.
def search_radius_time(request, latitude, longitude, year, month, day, hour, minute=0):
	# normalize timestamp
	timestamp = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute))
	n_timestamp = normalize_timestamp(timestamp)

	response = query(lat=float(lat), lon=float(lon), radius=float(radius), timestamp=[n_timestamp])
	return HttpResponse(json.dumps(response), content_type="application/json")
'''
def search(request, latitude=None, longitude=None, radius=None, year=None, month=None, day=None, hour=None, minute=None):
	if (latitude is not None) and (longitude is not None) and (radius is not None):
		lat = float(latitude)
		lon = float(latitude)
		rad = float(radius)
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
			else:
				timestamp = datetime.datetime(int(year), int(month), int(day))
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
