import os
import sys
import httplib2
import json
import pyfoursquare 


CLIENT_ID = 'E5JK3GUTSGOXWSWBUH4YHAAY1SSEYU1XP5LW3SMRTEMJBGNE'
CLIENT_SECRET = '5RFOZFEF2JO4RMZEZIPJGW2XDD0VX2X3LKE4PJJPPBKEVIUV'
REDIRECT_URI = ''

default_geo = u'40.7,-74.0'


def main(argv):
	basic_auth = 'client_id=%s&client_secret=%s' % (CLIENT_ID, CLIENT_SECRET)
	api = API(basic_auth)
	result = api.venues_search(query='Burburinho', ll='-8.063542,-34.872891')
	print 'good'
	print json.dumps(result, indent=4)


if __name__ == '__main__':
    main(sys.argv)
