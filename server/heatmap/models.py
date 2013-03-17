from mongoengine import DynamicDocument, GeoPointField, DateTimeField

class Location(DynamicDocument):
	coordinates = GeoPointField(required=True)
	timestamp = DateTimeField(required=True)

	def __unicode__(self):
		return 'Coordinates: %s' % self.coordinates

	meta = {
        'ordering': ['timestamp'],
    }
