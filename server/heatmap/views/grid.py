from heatmap.views.normalization import *
from heatmap.models import *
from django.http import HttpResponse
from collections import OrderedDict
import json
import datetime
import time
from math import *

def add_to_grid(dict, lat, lon):
	if (lat, lon) in dict:
		dict[(lat, lon)] = dict[(lat, lon)] + 1
	else:
		dict[(lat, lon)] = 1

def grid_search(request, callback=None, resolution):
	locations = Location.objects

	response = OrderedDict()
	for location in locations:
		n_timestamp = normalize_timestamp_to_hour(location.timestamp)
		n_timestamp_str = n_timestamp.strftime('%Y-%m-%d %H:%M:%S')

		if n_timestamp_str not in response:
			response[n_timestamp_str] = {}

		gridified_lat, gridified_lon = normalize_to_grid_center(lat, lon, resolution)
		add_to_grid(response[n_timestamp_str], gridified_lat, gridified_lon)

	if callback is None:
		return HttpResponse(json.dumps(response), content_type="application/json")
	else:
		return HttpResponse(callback+'('+json.dumps(response)+')', content_type="application/json")

def grid_search_region(request, callback=None, resolution, lat, lon, latrange, lonrange, resolution):
	locations = Location.objects
	grid_lat_index_min, grid_lon_index_min = gridify(lat-latrange/2, lon-lonrange/2, resolution)
	grid_lat_index_max, grid_lon_index_max = gridify(lat+latrange/2, lon-lonrange/2, resolution)

	response = OrderedDict()
	for location in locations:
		n_timestamp = normalize_timestamp_to_hour(location.timestamp)
		n_timestamp_str = n_timestamp.strftime('%Y-%m-%d %H:%M:%S')
		grid_lat_index, grid_lon_index = gridify(location.coordinates[0], location.coordinates[1], resolution)

		if (grid_lat_index >= grid_lat_index_min) and (grid_lat_index <= grid_lat_index_max) and (grid_lon_index >= grid_lon_index_min) and (grid_lon_index <= grid_lon_index_max):
			if n_timestamp_str not in response:
				response[n_timestamp_str] = {}

			gridified_lat, gridified_lon = grid_center(grid_lat_index, grid_lon_index, resolution)
			add_to_grid(response[n_timestamp_str], gridified_lat, gridified_lon)

	if callback is None:
		return HttpResponse(json.dumps(response), content_type="application/json")
	else:
		return HttpResponse(callback+'('+json.dumps(response)+')', content_type="application/json")

def grid_search_region_to_now(request, callback=None, resolution, lat, lon, latrange, lonrange, year, month, day, hour):
	locations = Location.objects
	from_timestamp = datetime.datetime(int(year), int(month), int(day), int(hour))

	response = OrderedDict()
	for location in locations:
		n_timestamp = normalize_timestamp_to_hour(location.timestamp)
		n_timestamp_str = n_timestamp.strftime('%Y-%m-%d %H:%M:%S')
		grid_lat_index, grid_lon_index = gridify(location.coordinates[0], location.coordinates[1], resolution)

		if (n_timestamp >= from_timestamp):
			if (grid_lat_index >= grid_lat_index_min) and (grid_lat_index <= grid_lat_index_max) and (grid_lon_index >= grid_lon_index_min) and (grid_lon_index <= grid_lon_index_max):
				if n_timestamp_str not in response:
					response[n_timestamp_str] = {}

				gridified_lat, gridified_lon = grid_center(grid_lat_index, grid_lon_index, resolution)
				add_to_grid(response[n_timestamp_str], gridified_lat, gridified_lon)

	if callback is None:
		return HttpResponse(json.dumps(response), content_type="application/json")
	else:
		return HttpResponse(callback+'('+json.dumps(response)+')', content_type="application/json")


def grid_search_region_in_timeframe(request, callback=None, resolution, lat, lon, latrange, lonrange, fyear, fmonth, fday, fhour, tyear, tmonth, tday, thour):
	locations = Location.objects
	from_timestamp = datetime.datetime(int(fyear), int(fmonth), int(fday), int(fhour))
	to_timestamp = datetime.datetime(int(tyear), int(tmonth), int(tday), int(thour))

	response = OrderedDict()
	for location in locations:
		n_timestamp = normalize_timestamp_to_hour(location.timestamp)
		n_timestamp_str = n_timestamp.strftime('%Y-%m-%d %H:%M:%S')
		grid_lat_index, grid_lon_index = gridify(location.coordinates[0], location.coordinates[1], resolution)

		if (n_timestamp >= from_timestamp) and (n_timestamp <= to_timestamp):
			if (grid_lat_index >= grid_lat_index_min) and (grid_lat_index <= grid_lat_index_max) and (grid_lon_index >= grid_lon_index_min) and (grid_lon_index <= grid_lon_index_max):
				if n_timestamp_str not in response:
					response[n_timestamp_str] = {}

				gridified_lat, gridified_lon = grid_center(grid_lat_index, grid_lon_index, resolution)
				add_to_grid(response[n_timestamp_str], gridified_lat, gridified_lon)

	if callback is None:
		return HttpResponse(json.dumps(response), content_type="application/json")
	else:
		return HttpResponse(callback+'('+json.dumps(response)+')', content_type="application/json")