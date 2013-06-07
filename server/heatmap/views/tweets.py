from twitter_scrape.models import TwitterLocation
from django.http import HttpResponse
from heatmap.views.normalization import *
import json
import datetime
import time

def twitter_reverse_geocode(request, lat, lon, radius, fyear, fmonth, fday, fhour, tyear, tmonth, tday, thour):
    #TODO factor in from_time and to_time
    lat = float(lat)
    lon = float(lon)
    radius = float(radius)
    from_timestamp = datetime.datetime(int(fyear), int(fmonth), int(fday), int(fhour))
    to_timestamp = datetime.datetime(int(tyear), int(tmonth), int(tday), int(thour))

    bottom_left_lon, bottom_left_lat = convert_to_bottom_left(lon, lat, radius, radius)
    upper_right_lon, upper_right_lat = convert_to_upper_right(lon, lat, radius, radius)
    results = TwitterLocation.objects(__raw__={
        'coordinates' : {'$within' : {'$box' : [ [bottom_left_lat, bottom_left_lon],[upper_right_lat, upper_right_lon] ]}},
        'timestamp' : { '$gte' : from_timestamp, '$lt' : to_timestamp + datetime.timedelta(hours = 1) }}).limit(25)

    reponse = []
    for result in results:
        response.append(result.tweet_text)
        if len(response) == 5:
            break

    json_response = {}

    #TODO construct_request_dict
    request_dict = construct_request_dict("")
    json_response["request"] = request_dict
    json_response["response"] = response
    return HttpResponse(json.dumps(json_response), content_type="application/json")

