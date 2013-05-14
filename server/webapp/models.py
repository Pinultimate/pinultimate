from django.contrib.auth import models
from models import User

class WebUser(models.Model):
    user = models.ForeignKey(User)
    total_taps = models.IntegerField(default=0)
    total_seconds_spent = models.IntegerField(default=0)
    total_logins = models.IntegerField(default=0)
