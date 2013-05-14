from analytics.models import *
from datetime import datetime
import json

def create_user(request, username):
	if request.method == 'POST':
		user = User(username=username)
		user.save()

def user_login(request, username):
	if request.method == 'POST':
		session = UsageSession(username=username, login=datetime.now())

def user_logout(request):
	return None

def user_touch(request, username):
	if request.method == 'POST':
		user = User.objects(username=username)
		if user is not None:
			
		else:
			# return user_not_found message