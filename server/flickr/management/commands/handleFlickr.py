from django.core.management.base import BaseCommand
import json, urllib2
from flickr.models import FlickrLocation
from server.settings import DBNAME
import mongoengine as mongo
import datetime
import time

API_KEY = 'c713991eeaef515a3fdacafdc0a140c4'
LAT = 37.4419
LON = -122.1419
QUERYSTRING_FORMAT = 'http://api.flickr.com/services/rest/?method=flickr.photos.search&per_page=250&license=0,1,2,3,4,5,6,7&has_geo=1&extras=original_format,tags,description,geo,date_taken,date_upload,owner_name,place_url&format=json&nojsoncallback=1&api_key={0}&lat={1}&lon={2}&min_upload_date={3}&page={4}'

def write_to_db(json_data):
    #make sure to count all pics by the same user in one hour as one 'checkin'
    for elem in json_data:
        userid = elem['ownername'];
        time = datetime.datetime.fromtimestamp(int(time.mktime(time.strptime(elem['datetaken'], "%Y-%m-%d %H:%M:%S"))))
        delta = datetime.timedelta(hours=0.5)
        same_users = FlickrLocation.objects(user_id=userid, timestamp__lte=time+delta, timestamp__gte=time-delta);
        if len(same_users) == 0:
            location = FlickrLocation(
                coordinates = [elem['latitude'], elem['longitude']],
                timestamp = time,
                user_id = userid,
            )
            location.save()

def get_min_upload_date():
    return 0;
    
def main():
    page = 1
    querystring = QUERYSTRING_FORMAT.format(API_KEY, LAT, LON, get_min_upload_date(), page)
        
    while page < 1000:
        print 'getting page #{0}'.format(page)
        data = json.loads(str(urllib2.urlopen(querystring).read()))
        write_to_db(data['photos']['photo']);
        if page >= int(data['photos']['pages']):
            break;
        page += 1
        querystring = QUERYSTRING_FORMAT.format(API_KEY, LAT, LON, get_min_upload_date(), page)
            

class Command(BaseCommand):
    def handle(self, *args, **options):
        mongo.connect(DBNAME)
        main()

