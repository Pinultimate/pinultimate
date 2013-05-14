from django.db import models as m
from django.contrib.sessions.models import Session
from datetime import datetime

class WebUser(Session):
    session = m.ForeignKey(Session)
    total_taps = m.IntegerField(default=0)
    total_seconds_spent = m.IntegerField(default=0)
    total_visits = m.IntegerField(default=0)
    last_updated = m.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.session

    def update(self):
        now = datetime.now()
        lapse = now - self.last_updated
        self.total_seconds_spent += lapse.seconds
        self.last_updated = now
        self.save()

    def tap(self):
        self.total_taps += 1
        self.update()