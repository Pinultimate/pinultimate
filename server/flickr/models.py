from mongoengine import DynamicDocument, GeoPointField, DateTimeField, StringField

class Location(DynamicDocument):
    coordinates = GeoPointField(required=True)
    timestamp = DateTimeField(required=True)
    time_added_to_db = DateTimeField(required=True)
    
    def __unicode__(self):
        return 'Coordinates: %s' % self.coordinates
    
    meta = {
        'ordering': ['timestamp'],
    }
    
class FlickrLocation(Location):
    source = StringField(default="flickr")
    user_id = StringField()
