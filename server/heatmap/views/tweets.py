from twitter_scrape.models import TwitterLocation
from django.http import HttpResponse
import json
import datetime
import time

def twitter_reverse_geocode(request, lat, lon, radius, fyear, fmonth, fday, fhour, tyear, tmonth, tday, thour):
    #TODO factor in from_time and to_time
    lat = float(lat)
    lon = float(lon)
    radius = float(radius)
    results = TwitterLocation.objects(coordinates__within_distance=[(lat, lon), radius]).limit(25)
    response = [result.tweet_text for result in results]
    json_response = {}
    #TODO construct_request_dict
    request_dict = construct_request_dict("")
    json_response["request"] = request_dict
    json_response["response"] = response
    return HttpResponse(json.dumps(json_response), content_type="application/json")

