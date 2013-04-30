from mongoengine import DynamicDocument, GeoPointField, DateTimeField, StringField

class Location(DynamicDocument):
    coordinates = GeoPointField(required=True)
    timestamp = DateTimeField(required=True)
    time_added_to_db = DateTimeField(required=True)
    source = StringField(default="unknown")

    def __unicode__(self):
        return 'Coordinates: %s' % self.coordinates

    meta = {
        'ordering': ['timestamp'],
    }

class FlickrLocation(Location):
    user_id = StringField()
