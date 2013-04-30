from mongoengine import StringField, IntField, ListField
from heatmap.models import Location

class TwitterLocation(Location):
    tweet = StringField()
    retweet_count = IntField()
    favorite_count = IntField()
    hashtags = ListField()
    user_id = StringField()
