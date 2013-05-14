from webapp.models import WebUser

def tap(request):
	if request.method == 'POST':
		web_user = WebUser.objects.get(session=request.session)
		if web_user is not None:
			web_user.tap()

def update(request):
	if request.method == 'POST':
		web_user = WebUser.objects.get(session=request.session)
		if web_user is not None:
			web_user.update()