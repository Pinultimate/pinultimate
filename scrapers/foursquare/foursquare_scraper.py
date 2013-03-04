import os
import sys
import httplib2
import json
import foursquare
import unittest


CLIENT_ID = 'E5JK3GUTSGOXWSWBUH4YHAAY1SSEYU1XP5LW3SMRTEMJBGNE'
CLIENT_SECRET = '5RFOZFEF2JO4RMZEZIPJGW2XDD0VX2X3LKE4PJJPPBKEVIUV'


LAT_BASE = 40.731649
LNG_BASE = -74.009399

LAT_LIMIT = 40.944639
LNG_LIMIT = -73.843231

RADIUS = 50
GAP = 111000 / RADIUS


def main(argv):
	geo_lat = []
	geo_lng = []
	checkinsCount = []
	hereNow = []
	usersCount = []
	venue_count = 0

	client = foursquare.Foursquare(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

	lat_length = (int)(GAP * (LAT_LIMIT - LAT_BASE))
	lng_length = (int)(GAP * (LNG_LIMIT - LNG_BASE))
	print lat_length
	print lng_length

	for i in xrange(lat_length):
		for j in xrange(lng_length): 
			newLat = LAT_BASE + float(i) / GAP
			newLng = LNG_BASE + float(j) / GAP
			geo = str(newLat) + ',' + str(newLng)
			print geo
			result = client.venues.search(params={'ll': geo, 'llAcc': 50, 'radius': RADIUS, 'limit': 50})
			for venue in result['venues']:
				venue_count += 1
				checkinsCount.append(venue['stats']['checkinsCount'])
				usersCount.append(venue['stats']['usersCount'])
				hereNow.append(venue['hereNow']['count'])
				geo_lng.append(venue['location']['lng'])
				geo_lat.append(venue['location']['lat'])
	print checkinsCount
	print usersCount
	print hereNow
	print venue_count


if __name__ == '__main__':
    main(sys.argv)
