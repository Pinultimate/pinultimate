import json, urllib2
from heatmap.models import InstagramLocation
from server.settings import DBNAME
import mongoengine as mongo

class InstagramPOSTHandler:

    def __init__(self):
        self.min_id = 0
        mongo.connect(DBNAME)

    def process(self, raw_post_data, client_id):
        object_id = '{none}'
        post_data = json.loads(str(raw_post_data))
        object_id = post_data[0]['object_id']
        querystring = 'https://api.instagram.com/v1/geographies/{0}/media/recent?client_id={1}&min_id={2}'.format(object_id, client_id, self.min_id)
        updated_data = urllib2.urlopen(querystring).read()
        data = json.loads(str(updated_data))
        self.write_to_db(data['data']);
        try:
            self.min_id = int(data['pagination']['next_min_id'])
        except:
            self.min_id = 0

    #data is a json array of the most recently updated posts, may already have entries in db
    def write_to_db(self, data):
        for elem in data:
            #first need to check if user is already in db for that time
            location = InstagramLocation(
                coordinates = [elem['location']['latitude'], elem['location']['longitude']],
                timestamp = elem['created_time'],
                user_id = elem['user']['id'],
            )
            location.save()
        
        
