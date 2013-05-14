from django.contrib.auth import models
from models import User
from datetime import datetime

class WebUser(models.Model):
    user = models.ForeignKey(User)
    total_taps = models.IntegerField(default=0)
    total_seconds_spent = models.IntegerField(default=0)
    total_logins = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
    	return user

	def update(self):
		now = datetime.now()
		lapse = now - self.last_updated
		self.total_seconds_spent += lapse.seconds
		self.last_updated = now
		self.save()

    def tap(self):
        self.total_taps += 1
        self.update()