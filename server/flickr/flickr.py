import json, urllib2
from heatmap.models import InstagramLocation
from server.settings import DBNAME
import mongoengine as mongo

API_KEY = 'c713991eeaef515a3fdacafdc0a140c4'
LAT = 37.4419
LON = -122.1419
QUERYSTRING_FORMAT = 'http://api.flickr.com/services/rest/?method=flickr.photos.search&per_page=250&license=0,1,2,3,4,5,6,7&has_geo=1&extras=original_format,tags,description,geo,date_taken,date_upload,owner_name,place_url&format=json&nojsoncallback=1&api_key={0}&lat={1}&lon={2}&min_upload_date={3}&page={4}'

def write_to_db(json_data):
    #make sure to count all pics by the same user in one hour as one 'checkin'
    for elem in json_data:
        date_taken = int(time.mktime(time.strptime(elem['datetaken'], "%Y-%m-%d %H:%M:%S")))
        location = FlickrLocation(
            coordinates = [elem['latitude'], elem['longitude']],
            timestamp = date_taken,
            user_id = elem['ownername'],
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
        print int(data['photos']['pages'])
        write_to_db(data['photos']['photo']);
        if page >= int(data['photos']['pages']):
            break;
        page += 1
        querystring = QUERYSTRING_FORMAT.format(API_KEY, LAT, LON, get_min_upload_date(), page)
            

if __name__ == '__main__':
    main()
