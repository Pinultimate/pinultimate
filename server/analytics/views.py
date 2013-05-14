from webapp.models import WebUser
from django.contrib.auth.decorators import login_required

@login_required()
def tap(request):
	if request.method == 'POST':
		web_user = WebUser.objects.get(user=request.user)
		if web_user is not None:
			web_user.tap()

@login_required()
def update(request):
	if request.method == 'POST':
		web_user = WebUser.objects.get(user=request.user)
		if web_user is not None:
			web_user.update()