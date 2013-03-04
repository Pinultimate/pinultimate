import oauth2 as oauth
import json
import math

CONSUMER_KEY = 'zEeYqSgskeQPiuX1J1tttg'
CONSUMER_SECRET = 'ZEA9YCnQ8PQ8k06kLyaBBXJXCFppcGvgMi7xpslRmI'

SEARCH_URL = "https://api.twitter.com/1.1/search/tweets.json"
GEOCODE_URL = "https://api.twitter.com/1.1/geo/search.json"

ACCESS_KEY = '236588284-SzCOK2fOC6IPYrcW0e72wxj6Zv1oe0wtflRVM3hk'
ACCESS_SECRET = 'AibVTmxw7NHNpBfY4VydC5Qe63zXBq95JdlJVBSV4'

def oauth_req(url, key, secret, http_method="GET", post_body=None, http_headers=None):
    
    consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    token = oauth.Token(key=key, secret=secret)
    client = oauth.Client(consumer, token)
    #print url

    resp, content = client.request(
        url,
        method=http_method,
        body=post_body,
        headers=http_headers,
        force_auth_header=True
    )
    return content

def oauth_get_req_with_params(url,key,secret,params):

    url_with_params = url + "?"
    for params_key in params.keys():
        url_with_params += params_key + "=" + str(params[params_key]) + "&"
    # Remove extraneous '?' or '&'
    url_with_params = url_with_params[:-1]
    return oauth_req(url_with_params,key,secret)

# EXAMPLE 1: Reverse Geo-encode --> find place based on coordinates

params = {
    'lat' : '37.4470610984003',
    'long' : '-122.160917799844',
    'granularity' : 'poi'
}

# Get JSON Response
geo_location_json_str = oauth_get_req_with_params(
    GEOCODE_URL,ACCESS_KEY,ACCESS_SECRET,params
)

# Convert JSON response to dict
geo_location_dict = json.loads(geo_location_json_str)

# Print results
geo_location_results = geo_location_dict["result"]["places"]
for place in geo_location_results:
    full_name = place["full_name"]
    id = place["id"]
    place_type = place["place_type"]
    print "Full Name: " + full_name
    print "ID: " + id
    print "Place Type: " + place_type

# EXAMPLE 2: Search Tweets near Cheesecake factory

#Longitude and Latitude caluclations from http://www.movable-type.co.uk/scripts/latlong.html
R = 6371 #km (Earth's radius)

# Don't use these calulate_new_latitude and longitude methods, they are really busted

# Bearing is given in radians, distance in km
def calculate_new_latitude(old_latitude,bearing,distance):
    return math.asin( math.sin(old_latitude)*math.cos(distance/R) + 
              math.cos(old_latitude)*math.sin(distance/R)*math.cos(bearing) );

# Dependent on both old and new latitude
def calculate_new_longitude(old_longitude,old_latitude,new_latitude,bearing,distance):
    return old_longitude + math.atan2(math.sin(bearing)*math.sin(distance/R)*math.cos(old_latitude), 
                     math.cos(distance/R)-math.sin(old_latitude)*math.sin(new_latitude));

def getLatitudeFromTweetParameters(tweet_search_params):
    geocode_string = tweet_search_params["geocode"]
    geocode_components = geocode_string.split(',')
    return float(geocode_components[0])

def setLatitudeForTweetParameters(tweet_search_params, latitude):
    geocode_string = tweet_search_params["geocode"]
    geocode_components = geocode_string.split(',')
    geocode_components[0] = str(latitude)
    tweet_search_params["geocode"] = ','.join(geocode_components)

def getLongitudeFromTweetParameters(tweet_search_params):
    geocode_string = tweet_search_params["geocode"]
    geocode_components = geocode_string.split(',')
    return float(geocode_components[1])

def setLongitudeForTweetParameters(tweet_search_params, longitude):
    geocode_string = tweet_search_params["geocode"]
    geocode_components = geocode_string.split(',')
    geocode_components[1] = str(longitude)
    tweet_search_params["geocode"] = ','.join(geocode_components)

tweets_search_params = {
    'q' : "%20", # Hack to search all tweets (that contain a space)
    'geocode' : "37.4470610984003,-122.160917799844,0.05km", # Within 50 meters of cheesecake factory
    'result_type' : 'recent'
}

longitude_delta = .0001

total_points = 50
points_so_far = 0
while (points_so_far < total_points):
    print "Points Tested: " + str(points_so_far)
    tweets_search_results_json_str = oauth_get_req_with_params(SEARCH_URL,ACCESS_KEY,ACCESS_SECRET,tweets_search_params)
    tweets_search_dict = json.loads(tweets_search_results_json_str)
    for status in tweets_search_dict["statuses"]:
        print "Tweet: " + status["text"]
        print "Full Name Of Place: " + place["full_name"]
        print "Place Type: " + place["place_type"]
    old_latitude = getLatitudeFromTweetParameters(tweets_search_params)
    old_longitude = getLongitudeFromTweetParameters(tweets_search_params)
    new_latitude = old_latitude
    new_longitude = old_longitude + longitude_delta
    print "New Latitude: " + str(new_latitude)
    print "New Longitude: " + str(new_longitude)

    #Set new lat and longitude
    setLatitudeForTweetParameters(tweets_search_params,new_latitude)
    setLongitudeForTweetParameters(tweets_search_params,new_longitude)

    #Update points
    points_so_far = points_so_far + 1

# Get JSON response
tweets_search_results_json_str = oauth_get_req_with_params(
    SEARCH_URL,ACCESS_KEY,ACCESS_SECRET,tweets_search_params
)
