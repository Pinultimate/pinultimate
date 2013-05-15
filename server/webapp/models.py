from django.db import models
from django.contrib.sessions.models import Session
from datetime import datetime
from django.utils.timezone import utc

class WebUser(models.Model):
    session = models.ForeignKey(Session, unique=True)
    total_taps = models.IntegerField(default=0)
    total_seconds_spent = models.IntegerField(default=0)
    total_visits = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.session

    def update(self):
        now = datetime.utcnow().replace(tzinfo=utc)
        lapse = now - self.last_updated
        self.total_seconds_spent += lapse.seconds
        self.last_updated = now
        self.save()

    def tap(self):
        self.total_taps += 1
        self.update()
