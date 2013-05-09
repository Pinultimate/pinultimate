from heatmap.views.normalization import *
from heatmap.views.requestdict import *
from heatmap.models import *
from django.http import HttpResponse
from collections import OrderedDict
import json
import datetime
import time
import sys
from django.db.models import Q
from math import *

def add_raw_location_to_list(location_list, gridified_lat, gridified_lon):
	location_list.append({"latitude" : gridified_lat, "longitude" : gridified_lon})	

def search(request, callback=None):
	locations = Location.objects

	json_response = {}
	json_response["request"] = construct_request_dict("raw")
	response = []

	prev_n_timestamp_str = None
	for location in locations:
		n_timestamp = normalize_timestamp_to_hour(location.timestamp)
		n_timestamp_str = n_timestamp.strftime('%Y-%m-%d %H:%M:%S')
		
		if prev_n_timestamp_str is None or prev_n_timestamp_str != n_timestamp_str:
			timestamp_response = {}
			response.append(timestamp_response)
			timestamp_response["timestamp"] = n_timestamp_str
			timestamp_response["locations"] = []
			add_raw_location_to_list(timestamp_response["locations"], location.coordinates[0], location.coordinates[1])
			prev_n_timestamp_str = n_timestamp_str
		else:
			prev_timestamp_response = response[-1]
			add_raw_location_to_list(prev_timestamp_response["locations"], location.coordinates[0], location.coordinates[1])

	json_response["response"] = response
	if callback is None:
		return HttpResponse(json.dumps(json_response), content_type="application/json")
	else:
		return HttpResponse(callback+'('+json.dumps(json_response)+')', content_type="application/json")

def in_range_from_center(target, c, r):
	if (target <= c + r/2) and (target >= c - r/2):
		return True
	else:
		return False

def search_region(request, lat, lon, latrange, lonrange, callback=None):
	# TODO: search within grid
	#locations = Location.objects
	lat = float(lat)
	lon = float(lon)
	latrange = float(latrange)
	lonrange = float(lonrange)
	
	bottom_left_lon, bottom_left_lat = convert_to_bottom_left(lon, lat, lonrange, latrange)
	upper_right_lon, upper_right_lat = convert_to_upper_right(lon, lat, lonrange, latrange)
	locations = Location.objects(coordinates__within_box=[(bottom_left_lat, bottom_left_lon), (upper_right_lat, upper_right_lon)])
	json_response = {}
	request_dict = construct_request_dict("raw")
	append_region(request_dict, lat, lon, latrange, lonrange)
	json_response["request"] = request_dict
	response = []

	prev_n_timestamp_str = None
	for location in locations:
		n_timestamp = normalize_timestamp_to_hour(location.timestamp)
		n_timestamp_str = n_timestamp.strftime('%Y-%m-%d %H:%M:%S')

		if (in_range_from_center(location.coordinates[0], lat, latrange)) and (in_range_from_center(location.coordinates[1], lon, lonrange)):
			if prev_n_timestamp_str is None or prev_n_timestamp_str != n_timestamp_str:
				timestamp_response = {}
				response.append(timestamp_response)
				timestamp_response["timestamp"] = n_timestamp_str
				timestamp_response["locations"] = []
				add_raw_location_to_list(timestamp_response["locations"], location.coordinates[0], location.coordinates[1])
				prev_n_timestamp_str = n_timestamp_str
			else:
				prev_timestamp_response = response[-1]
				add_raw_location_to_list(prev_timestamp_response["locations"], location.coordinates[0], location.coordinates[1])

	json_response["response"] = response
	if callback is None:
		return HttpResponse(json.dumps(json_response), content_type="application/json")
	else:
		return HttpResponse(callback+'('+json.dumps(json_response)+')', content_type="application/json")

def search_region_to_now(request, lat, lon, latrange, lonrange, year, month, day, hour, callback=None):
	#locations = Location.objects
	lat = float(lat)
	lon = float(lon)
	latrange = float(latrange)
	lonrange = float(lonrange)

	from_timestamp = datetime.datetime(int(year), int(month), int(day), int(hour))
	bottom_left_lon, bottom_left_lat = convert_to_bottom_left(lon, lat, lonrange, latrange)
	upper_right_lon, upper_right_lat = convert_to_upper_right(lon, lat, lonrange, latrange)
	locations = Location.objects(__raw__={
		'coordinates' : {'$within' : { '$box' : [ [bottom_left_lat, bottom_left_lon], [upper_right_lat, upper_right_lon] ] }},
		'timestamp' : { '$gte' : from_timestamp }})
	
	json_response = {}
	request_dict = construct_request_dict("raw")
	append_region(request_dict, lat, lon, latrange, lonrange)
	append_from_time(request_dict, from_timestamp)
	append_to_time(request_dict, datetime.datetime.now())
	json_response["request"] = request_dict
	response = []

	prev_n_timestamp_str = None
	for location in locations:
		n_timestamp = normalize_timestamp_to_hour(location.timestamp)
		n_timestamp_str = n_timestamp.strftime('%Y-%m-%d %H:%M:%S')

		if (in_range_from_center(location.coordinates[0], lat, latrange)) and (in_range_from_center(location.coordinates[1], lon, lonrange)):
			if (n_timestamp >= from_timestamp):
				if prev_n_timestamp_str is None or prev_n_timestamp_str != n_timestamp_str:
					timestamp_response = {}
					response.append(timestamp_response)
					timestamp_response["timestamp"] = n_timestamp_str
					timestamp_response["locations"] = []
					add_raw_location_to_list(timestamp_response["locations"], location.coordinates[0], location.coordinates[1])
					prev_n_timestamp_str = n_timestamp_str
				else:
					prev_timestamp_response = response[-1]
					add_raw_location_to_list(prev_timestamp_response["locations"], location.coordinates[0], location.coordinates[1])

	json_response["response"] = response
	if callback is None:
		return HttpResponse(json.dumps(json_response), content_type="application/json")
	else:
		return HttpResponse(callback+'('+json.dumps(json_response)+')', content_type="application/json")


def search_region_in_timeframe(request, lat, lon, latrange, lonrange, fyear, fmonth, fday, fhour, tyear, tmonth, tday, thour, callback=None):
	#locations = Location.objects
	lat = float(lat)
	lon = float(lon)
	latrange = float(latrange)
	lonrange = float(lonrange)

	from_timestamp = datetime.datetime(int(fyear), int(fmonth), int(fday), int(fhour))
	to_timestamp = datetime.datetime(int(tyear), int(tmonth), int(tday), int(thour))
	bottom_left_lon, bottom_left_lat = convert_to_bottom_left(lon, lat, lonrange, latrange)
	upper_right_lon, upper_right_lat = convert_to_upper_right(lon, lat, lonrange, latrange)
	locations = Location.objects(__raw__={
		'coordinates' : {'$within' : { '$box' : [ [bottom_left_lat, bottom_left_lon], [upper_right_lat, upper_right_lon] ] }},
		'timestamp' : { '$gte' : from_timestamp, '$lt' : to_timestamp + datetime.timedelta(hours = 1) }})

	json_response = {}
	request_dict = construct_request_dict("raw")
	append_region(request_dict, lat, lon, latrange, lonrange)
	append_from_time(request_dict, from_timestamp)
	append_to_time(request_dict, to_timestamp)
	json_response["request"] = request_dict
	response = []

	prev_n_timestamp_str = None
	for location in locations:
		n_timestamp = normalize_timestamp_to_hour(location.timestamp)
		n_timestamp_str = n_timestamp.strftime('%Y-%m-%d %H:%M:%S')

		if (in_range_from_center(location.coordinates[0], lat, latrange)) and (in_range_from_center(location.coordinates[1], lon, lonrange)):
			if (n_timestamp >= from_timestamp) and (n_timestamp <= to_timestamp):
				if prev_n_timestamp_str is None or prev_n_timestamp_str != n_timestamp_str:
					timestamp_response = {}
					response.append(timestamp_response)
					timestamp_response["timestamp"] = n_timestamp_str
					timestamp_response["locations"] = []
					add_raw_location_to_list(timestamp_response["locations"], location.coordinates[0], location.coordinates[1])
					prev_n_timestamp_str = n_timestamp_str
				else:
					prev_timestamp_response = response[-1]
					add_raw_location_to_list(prev_timestamp_response["locations"], location.coordinates[0], location.coordinates[1])

	json_response["response"] = response
	if callback is None:
		return HttpResponse(json.dumps(json_response), content_type="application/json")
	else:
		return HttpResponse(callback+'('+json.dumps(json_response)+')', content_type="application/json")

