import datetime
from heatmap.views.normalization import *

def construct_request_dict(query_type):
	request_dict = {"data_type" : query_type, "requested_time" : str(normalize_timestamp_to_minute(datetime.datetime.now()))}
	return request_dict

def append_region(request_dict, lat, lon, latrange, lonrange):
	request_dict["latitude"] = lat
	request_dict["longitude"] = lon
	request_dict["latrange"] = latrange
	request_dict["lonrange"] = lonrange

def append_from_time(request_dict, from_timestamp):
	request_dict["from"] = str(normalize_timestamp_to_minute(from_timestamp))

def append_to_time(request_dict, to_timestamp):
	request_dict["to"] = str(normalize_timestamp_to_minute(to_timestamp))