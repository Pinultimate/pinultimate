from mongoengine import StringField
from heatmap.models import Location


class InstagramLocation(Location):
    user_id = StringField()
