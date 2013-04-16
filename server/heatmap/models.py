from mongoengine import DynamicDocument, GeoPointField, DateTimeField, StringField

class Location(DynamicDocument):
	coordinates = GeoPointField(required=True)
	timestamp = DateTimeField(required=True)

	def __unicode__(self):
		return 'Coordinates: %s' % self.coordinates

	meta = {
                'ordering': ['timestamp'],
        }

class InstagramLocation(Location):
        source = StringField(default="instagram")
        user_id = StringField()

class FlickrLocation(Location):
        source = StringField(default="flickr")
        user_id = StringField()
    
