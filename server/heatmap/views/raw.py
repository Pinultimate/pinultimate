from django.http import HttpResponse
from heatmap.models import *
from collections import OrderedDict
import json
import datetime
import time
from math import *

'''
# if a specific timestamp (1-hour-interval) has zero checkins, then that key-value pair is not included in the json
# radious: in degrees
# timestamps is a list
def query_radius(lat=None, lon=None, rad=None, timestamps=None, exp=False):
	response = OrderedDict()
	locations = Location.objects

	prev_timestamp = None
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
			if (exp is True) and (prev_timestamp is not None):
				time_diff = n_timestamp-prev_timestamp
				for missing_hour in range(1, int(time_diff.total_seconds()/3600) + 1):
					missing_timestamp = prev_timestamp + datetime.timedelta(hours=missing_hour)
					missing_timestamp_str = missing_timestamp.strftime('%Y-%m-%d %H:%M:%S')
					response[missing_timestamp_str] = []
				
			prev_timestamp = n_timestamp	
			response[n_timestamp_str] = []
		response[n_timestamp_str].append(location.coordinates)
	return response

def query_region(lat=None, lon=None, latrange=None, lonrange=None, timestamps=None, exp=False):
	response = OrderedDict()
	locations = Location.objects

	prev_timestamp = None
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
			if (exp is True) and (prev_timestamp is not None):
				time_diff = n_timestamp-prev_timestamp
				for missing_hour in range(1, int(time_diff.total_seconds()/3600) + 1):
					missing_timestamp = prev_timestamp + datetime.timedelta(hours=missing_hour)
					missing_timestamp_str = missing_timestamp.strftime('%Y-%m-%d %H:%M:%S')
					response[missing_timestamp_str] = []
				
			prev_timestamp = n_timestamp
			response[n_timestamp_str] = []
		response[n_timestamp_str].append(location.coordinates)
	return response
'''

def normalize_timestamp_to_hour(timestamp):
	return datetime.datetime(timestamp.year, timestamp.month, timestamp.day, timestamp.hour)

# does not explicitly append empty list for times with 0 check-in's
def search(request, callback=None):
	locations = Location.objects

	response = OrderedDict()
	for location in locations:
		n_timestamp = normalize_timestamp_to_hour(location.timestamp)
		n_timestamp_str = n_timestamp.strftime('%Y-%m-%d %H:%M:%S')
		if n_timestamp_str not in response:
			response[n_timestamp_str] = []

		response[n_timestamp_str].append(location.coordinates)

	if callback is None:
		return HttpResponse(json.dumps(response), content_type="application/json")
	else:
		return HttpResponse(callback+'('+json.dumps(response)+')', content_type="application/json")

def in_range_from_center(target, center, range):
	if (target <= center + range/2) or (target >= center - range/2):
		return True
	else
		return False

def search_region(request, callback=None, lat, lon, latrange, lonrange):
	locations = Location.objects

	response = OrderedDict()
	for location in locations:
		n_timestamp = normalize_timestamp_to_hour(location.timestamp)
		n_timestamp_str = n_timestamp.strftime('%Y-%m-%d %H:%M:%S')

		if (in_range_from_center(location.coordinates[0], lat, latrange)) and (in_range_from_center(location.coordinates[1], lon, lonrange)):
			if n_timestamp_str not in response:
				response[n_timestamp_str] = []

			response[n_timestamp_str].append(location.coordinates)

	if callback is None:
		return HttpResponse(json.dumps(response), content_type="application/json")
	else:
		return HttpResponse(callback+'('+json.dumps(response)+')', content_type="application/json")

def search_region_to_now(request, callback=None, lat, lon, latrange, lonrange, year, month, day, hour):
	locations = Location.objects
	from_timestamp = datetime.datetime(int(year), int(month), int(day), int(hour))

	response = OrderedDict()
	for location in locations:
		n_timestamp = normalize_timestamp_to_hour(location.timestamp)
		n_timestamp_str = n_timestamp.strftime('%Y-%m-%d %H:%M:%S')

		if (in_range_from_center(location.coordinates[0], lat, latrange)) and (in_range_from_center(location.coordinates[1], lon, lonrange)):
			if (n_timestamp >= from_timestamp):
				if n_timestamp_str not in response:
					response[n_timestamp_str] = []

				response[n_timestamp_str].append(location.coordinates)

	if callback is None:
		return HttpResponse(json.dumps(response), content_type="application/json")
	else:
		return HttpResponse(callback+'('+json.dumps(response)+')', content_type="application/json")


def search_region_in_timeframe(request, callback=None, lat, lon, latrange, lonrange, fyear, fmonth, fday, fhour, tyear, tmonth, tday, thour):
	locations = Location.objects
	from_timestamp = datetime.datetime(int(fyear), int(fmonth), int(fday), int(fhour))
	to_timestamp = datetime.datetime(int(tyear), int(tmonth), int(tday), int(thour))

	response = OrderedDict()
	for location in locations:
		n_timestamp = normalize_timestamp_to_hour(location.timestamp)
		n_timestamp_str = n_timestamp.strftime('%Y-%m-%d %H:%M:%S')

		if (in_range_from_center(location.coordinates[0], lat, latrange)) and (in_range_from_center(location.coordinates[1], lon, lonrange)):
			if (n_timestamp >= from_timestamp) and (n_timestamp <= to_timestamp):
				if n_timestamp_str not in response:
					response[n_timestamp_str] = []

				response[n_timestamp_str].append(location.coordinates)

	if callback is None:
		return HttpResponse(json.dumps(response), content_type="application/json")
	else:
		return HttpResponse(callback+'('+json.dumps(response)+')', content_type="application/json")

