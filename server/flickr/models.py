from mongoengine import StringField
from heatmap.models import Location

class FlickrLocation(Location):
    user_id = StringField()
