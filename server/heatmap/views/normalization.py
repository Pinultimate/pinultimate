def gridify(self, lat, lng reso):
	LAT_SHIFT = 90
	LNG_SHIFT = 180
	lng_index = math.floor((lng + LNG_SHIFT) / reso)
	lat_index = math.floor((-lat + LAT_SHIFT) / reso)
	return lat_index, lng_index

def grid_center(self, lat_index, lng_index, reso):
	LAT_SHIFT = 90
	LNG_SHIFT = 180
	lat = -(lat_index + 0.5) * reso + LAT_SHIFT
	lng = (lng_index + 0.5) * reso - LNG_SHIFT
	center = {'longitude': lng, 'latitude': lat}
	return center

def max_index(self, reso):
	return math.floor(180/reso), math.floor(360/reso)
