from django.db import models
from datetime import datetime
from django.utils.timezone import utc

class PhoneUser(models.Model):
    phone_id = models.CharField(max_length=100)
    total_taps = models.IntegerField(default=0)
    total_seconds_spent = models.IntegerField(default=0)
    total_visits = models.IntegerField(default=0)
    last_opened = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.phone_id

    def open_app(self):
        now = datetime.utcnow().replace(tzinfo=utc)
        self.total_visits += 1
        self.last_opened = now
        self.save()

    def close_app(self):
        now = datetime.utcnow().replace(tzinfo=utc)
        lapse = now - self.last_opened
        self.total_seconds_spent += lapse.seconds
        self.save()

    def tap(self):
        self.total_taps += 1
        self.save()