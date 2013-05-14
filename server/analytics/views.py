from webapp.models import WebUser

def tap(request, user_id):
	if request.method == 'POST':
		web_user = WebUser.objects.get(id=user_id)
		if user is not None:
			web_user.tap()

def update(request, user_id):
	if request.method == 'POST':
		web_user = WebUser.objects.get(id=user_id)
		if user is not None:
			web_user.update()