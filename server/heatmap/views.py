from django.http import HttpResponse
from heatmap.models import *
from collections import defaultdict
import json
import datetime
import time

# Create your views here.
def find_locations_radius_time(request, latitude, longitude, year, month, day, hour, minute):
	return HttpResponse("Latitude : %s\nLongitude : %s\nDatetime : %s/%s/%s, %s:%s" % (latitude, longitude, month, day, year, hour, minute))

def find_locations_radius(request, latitude, longitude):
	return HttpResponse("Latitude : %s\nLongitude : %s" % (latitude, longitude))

def find_locations_all(request):
	response = defaultdict(list)
	locations = Location.objects
	for location in locations:
		n_timestamp = normalize_timestamp(location.timestamp).strftime('%Y-%m-%d %H:%M:%S')
		response[n_timestamp].append(location.coordinates)
	return HttpResponse(json.dumps(response), content_type="application/json")

def add_location_now(request, latitude, longitude):
	location = Location(
		coordinates=[float(latitude), float(longitude)],
		timestamp=datetime.datetime.now(),
	)
	location.save()
	return HttpResponse('Added %s' % location.coordinates)

def normalize_timestamp(timestamp):
	# TODO: handle tzinfo if necessary in the future
	return datetime.datetime(timestamp.year, timestamp.month, timestamp.day, timestamp.hour)
	