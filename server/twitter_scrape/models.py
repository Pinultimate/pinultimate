from mongoengine import StringField, IntField, ListField
from heatmap.models import Location

class TwitterLocation(Location):
    tweet_text = StringField(required=True)
    retweet_count = IntField(required=True)
    favorite_count = IntField(required=True)
    user_id = StringField(required=True)
    hashtags = ListField()
