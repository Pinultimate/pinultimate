from heatmap.views.normalization import *
from heatmap.views.requestdict import *
from instagram.models import *
from flickr.models import *
from twitter_scrape.models import *
from heatmap.models import *
from django.http import HttpResponse
from collections import OrderedDict
import json
import datetime
import time
from django.db.models import Q
from math import *

def add_grid_location_to_list(location_list, gridified_lat, gridified_lon, source=None):
	for location in location_list:
		if location["latitude"] == gridified_lat and location["longitude"] == gridified_lon:
			location["count"] = location["count"] + 1
			if source is not None:
				location[source] = location[source] + 1
			return
	location = {"latitude" : gridified_lat, "longitude" : gridified_lon, "count" : 1, "instagram" : 0, "flickr" : 0, "twitter" : 0}
	location[source] = 1
	location_list.append(location)

def grid_search(request, resolution, callback=None):
	locations = Location.objects
	resolution = float(resolution)

	json_response = {}
	request_dict = construct_request_dict("grid")
	json_response["request"] = request_dict
	response = []

	prev_n_timestamp_str = None
	for location in locations:
		n_timestamp = normalize_timestamp_to_hour(location.timestamp)
		n_timestamp_str = n_timestamp.strftime('%Y-%m-%d %H:%M:%S')
		gridified_lat, gridified_lon = normalize_to_grid_center(location.coordinates[0], location.coordinates[1], resolution)

		if prev_n_timestamp_str is None or prev_n_timestamp_str != n_timestamp_str:			
			timestamp_response = {}
			response.append(timestamp_response)
			timestamp_response["timestamp"] = n_timestamp_str
			timestamp_response["locations"] = []
			add_grid_location_to_list(timestamp_response["locations"], gridified_lat, gridified_lon, location.source)
			prev_n_timestamp_str = n_timestamp_str
		else:
			prev_timestamp_response = response[-1]
			add_grid_location_to_list(prev_timestamp_response["locations"], gridified_lat, gridified_lon, location.source)

	json_response["response"] = response
	if callback is None:
		return HttpResponse(json.dumps(json_response), content_type="application/json")
	else:
		return HttpResponse(callback+'('+json.dumps(json_response)+')', content_type="application/json")

def grid_search_region(request, resolution, lat, lon, latrange, lonrange, callback=None):
	#locations = Location.objects
	lat = float(lat)
	lon = float(lon)
	latrange = float(latrange)
	lonrange = float(lonrange)
	resolution = float(resolution)

	bottom_left_lon, bottom_left_lat = convert_to_bottom_left(lon, lat, lonrange, latrange)
	upper_right_lon, upper_right_lat = convert_to_upper_right(lon, lat, lonrange, latrange)
	locations = Location.objects(coordinates__within_box=[(bottom_left_lat, bottom_left_lon), (upper_right_lat, upper_right_lon)])

	grid_lat_index_min, grid_lon_index_min = gridify(lat-latrange/2, lon-lonrange/2, resolution)
	grid_lat_index_max, grid_lon_index_max = gridify(lat+latrange/2, lon+lonrange/2, resolution)

	wrapping = False
	if grid_lon_index_max < grid_lon_index_min:
		wrapping = True
		grid_lon_index_max = grid_lon_index_max + max_lon_index(resolution)

	json_response = {}
	request_dict = construct_request_dict("grid")
	append_region(request_dict, lat, lon, latrange, lonrange)
	json_response["request"] = request_dict
	response = []

	prev_n_timestamp_str = None
	for location in locations:
		n_timestamp = normalize_timestamp_to_hour(location.timestamp)
		n_timestamp_str = n_timestamp.strftime('%Y-%m-%d %H:%M:%S')
		grid_lat_index, grid_lon_index = gridify(location.coordinates[0], location.coordinates[1], resolution)
		gridified_lat, gridified_lon = grid_center(grid_lat_index, grid_lon_index, resolution)

		if wrapping:
			if grid_lon_index < grid_lon_index_min:
				grid_lon_index = grid_lon_index + max_lon_index(resolution)

		if (grid_lat_index >= grid_lat_index_min) and (grid_lat_index <= grid_lat_index_max) and (grid_lon_index >= grid_lon_index_min) and (grid_lon_index <= grid_lon_index_max):
			if prev_n_timestamp_str is None or prev_n_timestamp_str != n_timestamp_str:
				timestamp_response = {}
				response.append(timestamp_response)
				timestamp_response["timestamp"] = n_timestamp_str
				timestamp_response["locations"] = []
				add_grid_location_to_list(timestamp_response["locations"], gridified_lat, gridified_lon, location.source)
				prev_n_timestamp_str = n_timestamp_str
			else:
				prev_timestamp_response = response[-1]
				add_grid_location_to_list(prev_timestamp_response["locations"], gridified_lat, gridified_lon, location.source)

	json_response["response"] = response
	if callback is None:
		return HttpResponse(json.dumps(json_response), content_type="application/json")
	else:
		return HttpResponse(callback+'('+json.dumps(json_response)+')', content_type="application/json")

def grid_search_region_to_now(request, resolution, lat, lon, latrange, lonrange, year, month, day, hour, callback=None):
	#locations = Location.objects
	lat = float(lat)
	lon = float(lon)
	latrange = float(latrange)
	lonrange = float(lonrange)
	resolution = float(resolution)
	
	from_timestamp = datetime.datetime(int(year), int(month), int(day), int(hour))
	bottom_left_lon, bottom_left_lat = convert_to_bottom_left(lon, lat, lonrange, latrange)
	upper_right_lon, upper_right_lat = convert_to_upper_right(lon, lat, lonrange, latrange)
	locations = Location.objects(__raw__={
		'coordinates' : {'$within' : { '$box' : [ [bottom_left_lat, bottom_left_lon], [upper_right_lat, upper_right_lon] ] }},
		'timestamp' : { '$gte' : from_timestamp }})

	grid_lat_index_min, grid_lon_index_min = gridify(lat-latrange/2, lon-lonrange/2, resolution)
	grid_lat_index_max, grid_lon_index_max = gridify(lat+latrange/2, lon+lonrange/2, resolution)

	wrapping = False
	if grid_lon_index_max < grid_lon_index_min:
		wrapping = True
		grid_lon_index_max = grid_lon_index_max + max_lon_index(resolution)

	json_response = {}
	request_dict = construct_request_dict("grid")
	append_region(request_dict, lat, lon, latrange, lonrange)
	append_from_time(request_dict, from_timestamp)
	append_to_time(request_dict, datetime.datetime.now())
	json_response["request"] = request_dict
	response = []

	prev_n_timestamp_str = None
	for location in locations:
		n_timestamp = normalize_timestamp_to_hour(location.timestamp)
		n_timestamp_str = n_timestamp.strftime('%Y-%m-%d %H:%M:%S')
		grid_lat_index, grid_lon_index = gridify(location.coordinates[0], location.coordinates[1], resolution)

		if wrapping:
			if grid_lon_index < grid_lon_index_min:
				grid_lon_index = grid_lon_index + max_lon_index(resolution)

		if (n_timestamp >= from_timestamp):
			if (grid_lat_index >= grid_lat_index_min) and (grid_lat_index <= grid_lat_index_max) and (grid_lon_index >= grid_lon_index_min) and (grid_lon_index <= grid_lon_index_max):
				gridified_lat, gridified_lon = grid_center(grid_lat_index, grid_lon_index, resolution)
				if prev_n_timestamp_str is None or prev_n_timestamp_str != n_timestamp_str:
					timestamp_response = {}
					response.append(timestamp_response)
					timestamp_response["timestamp"] = n_timestamp_str
					timestamp_response["locations"] = []
					add_grid_location_to_list(timestamp_response["locations"], gridified_lat, gridified_lon, location.source)
					prev_n_timestamp_str = n_timestamp_str
				else:
					prev_timestamp_response = response[-1]
					add_grid_location_to_list(prev_timestamp_response["locations"], gridified_lat, gridified_lon, location.source)

	json_response["response"] = response
	if callback is None:
		return HttpResponse(json.dumps(json_response), content_type="application/json")
	else:
		return HttpResponse(callback+'('+json.dumps(json_response)+')', content_type="application/json")


def grid_search_region_in_timeframe(request, resolution, lat, lon, latrange, lonrange, fyear, fmonth, fday, fhour, tyear, tmonth, tday, thour, callback=None):
	#locations = Location.objects
	lat = float(lat)
	lon = float(lon)
	latrange = float(latrange)
	lonrange = float(lonrange)
	resolution = float(resolution)
	
	from_timestamp = datetime.datetime(int(fyear), int(fmonth), int(fday), int(fhour))
	to_timestamp = datetime.datetime(int(tyear), int(tmonth), int(tday), int(thour))
	bottom_left_lon, bottom_left_lat = convert_to_bottom_left(lon, lat, lonrange, latrange)
	upper_right_lon, upper_right_lat = convert_to_upper_right(lon, lat, lonrange, latrange)
	locations = Location.objects(__raw__={
		'coordinates' : {'$within' : { '$box' : [ [bottom_left_lat, bottom_left_lon], [upper_right_lat, upper_right_lon] ] }},
		'timestamp' : { '$gte' : from_timestamp, '$lt' : to_timestamp + datetime.timedelta(hours = 1) }})

	grid_lat_index_min, grid_lon_index_min = gridify(lat-latrange/2, lon-lonrange/2, resolution)
	grid_lat_index_max, grid_lon_index_max = gridify(lat+latrange/2, lon+lonrange/2, resolution)

	wrapping = False
	if grid_lon_index_max < grid_lon_index_min:
		wrapping = True
		grid_lon_index_max = grid_lon_index_max + max_lon_index(resolution)

	json_response = {}
	request_dict = construct_request_dict("grid")
	append_region(request_dict, lat, lon, latrange, lonrange)
	append_from_time(request_dict, from_timestamp)
	append_to_time(request_dict, to_timestamp)
	json_response["request"] = request_dict
	response = []

	cur_timestamp = from_timestamp
	while cur_timestamp <= to_timestamp:
		cur_timestamp_str = cur_timestamp.strftime('%Y-%m-%d %H:%M:%S')
		timestamp_response = {}
		response.append(timestamp_response)
		timestamp_response["timestamp"] = cur_timestamp_str
		timestamp_response["locations"] = []
		cur_timestamp = cur_timestamp + timedelta(hours=1)

	for location in locations:
		n_timestamp = normalize_timestamp_to_hour(location.timestamp)
		n_timestamp_str = n_timestamp.strftime('%Y-%m-%d %H:%M:%S')
		grid_lat_index, grid_lon_index = gridify(location.coordinates[0], location.coordinates[1], resolution)

		if wrapping:
			if grid_lon_index < grid_lon_index_min:
				grid_lon_index = grid_lon_index + max_lon_index(resolution)

		if (n_timestamp >= from_timestamp) and (n_timestamp <= to_timestamp):
			if (grid_lat_index >= grid_lat_index_min) and (grid_lat_index <= grid_lat_index_max) and (grid_lon_index >= grid_lon_index_min) and (grid_lon_index <= grid_lon_index_max):				
				gridified_lat, gridified_lon = grid_center(grid_lat_index, grid_lon_index, resolution)				
				timestamp_response = response[n_timestamp_str]
				add_grid_location_to_list(timestamp_response["locations"], gridified_lat, gridified_lon, location.source)

	json_response["response"] = response
	if callback is None:
		return HttpResponse(json.dumps(json_response), content_type="application/json")
	else:
		return HttpResponse(callback+'('+json.dumps(json_response)+')', content_type="application/json")