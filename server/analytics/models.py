from django.db import models
from datetime import datetime

class PhoneUser(models.Model):
    phone_id = CharField(required=True)
    total_taps = models.IntegerField(default=0)
    total_seconds_spent = models.IntegerField(default=0)
    total_visits = models.IntegerField(default=0)
    last_opened = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.phone_id

    def open_app(self):
        now = datetime.now()
        self.total_visits += 1
        self.last_opened = now
        self.save()

    def close_app(self):
        now = datettime.now()
        lapse = now - self.last_opened
        self.total_seconds_spent += lapse
        self.save()

    def tap(self):
        self.total_taps += 1
        self.save()