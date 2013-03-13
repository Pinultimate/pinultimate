from django.db import models
from mongoengine import *

class Location(DynamicDocument):
	coordinates = GeoPointField(required=True)
	timestamp = DateTimeField(required=True)
	
	def __unicode__(self):
		return 'Coordinates: %s' % self.coordinates
	
	meta = {
        'ordering': ['timestamp'],
    }
