import os
import sys
import httplib2
import json
import foursquare

CLIENT_ID = 'E5JK3GUTSGOXWSWBUH4YHAAY1SSEYU1XP5LW3SMRTEMJBGNE'
CLIENT_SECRET = '5RFOZFEF2JO4RMZEZIPJGW2XDD0VX2X3LKE4PJJPPBKEVIUV'

def main(argv):
    client = foursquare.Foursquare(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    venues = client.venues('40a55d80f964a52020f31ee3')
    print json.dumps(venues, indent=4)

if __name__ == '__main__':
    main(sys.argv)
