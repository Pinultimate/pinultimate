def grid_search(request, callback=None):
	locations = Location.objects

	response = OrderedDict()
	for location in locations:
		n_timestamp = normalize_timestamp_to_hour(location.timestamp)
		n_timestamp_str = n_timestamp.strftime('%Y-%m-%d %H:%M:%S')




	if callback is None:
		return HttpResponse(json.dumps(response), content_type="application/json")
	else:
		return HttpResponse(callback+'('+json.dumps(response)+')', content_type="application/json")

def grid_search_region(request, callback=None, lat, lon, latrange, lonrange):
	locations = Location.objects

	response = OrderedDict()
	for location in locations:
		n_timestamp = normalize_timestamp_to_hour(location.timestamp)
		n_timestamp_str = n_timestamp.strftime('%Y-%m-%d %H:%M:%S')



	if callback is None:
		return HttpResponse(json.dumps(response), content_type="application/json")
	else:
		return HttpResponse(callback+'('+json.dumps(response)+')', content_type="application/json")

def grid_search_region_to_now(request, callback=None, lat, lon, latrange, lonrange, year, month, day, hour):
	locations = Location.objects
	from_timestamp = datetime.datetime(int(year), int(month), int(day), int(hour))

	response = OrderedDict()
	for location in locations:
		n_timestamp = normalize_timestamp_to_hour(location.timestamp)
		n_timestamp_str = n_timestamp.strftime('%Y-%m-%d %H:%M:%S')




	if callback is None:
		return HttpResponse(json.dumps(response), content_type="application/json")
	else:
		return HttpResponse(callback+'('+json.dumps(response)+')', content_type="application/json")


def grid_search_region_in_timeframe(request, callback=None, lat, lon, latrange, lonrange, fyear, fmonth, fday, fhour, tyear, tmonth, tday, thour):
	locations = Location.objects
	from_timestamp = datetime.datetime(int(fyear), int(fmonth), int(fday), int(fhour))
	to_timestamp = datetime.datetime(int(tyear), int(tmonth), int(tday), int(thour))

	response = OrderedDict()
	for location in locations:
		n_timestamp = normalize_timestamp_to_hour(location.timestamp)
		n_timestamp_str = n_timestamp.strftime('%Y-%m-%d %H:%M:%S')





	if callback is None:
		return HttpResponse(json.dumps(response), content_type="application/json")
	else:
		return HttpResponse(callback+'('+json.dumps(response)+')', content_type="application/json")