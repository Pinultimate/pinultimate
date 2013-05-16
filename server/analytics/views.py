from webapp.models import WebUser
from django.contrib.sessions.models import Session
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@require_POST
def tap(request):
    session = Session.objects.get(session_key=request.session.session_key)
    web_user_queryset = WebUser.objects.filter(session=session)
    web_user = list(web_user_queryset)
    if web_user is not None and len(web_user) > 0:
        web_user = web_user[0]
        web_user.tap()
    return HttpResponse(status=200)


@csrf_exempt
@require_POST
def update(request):
    session = Session.objects.get(session_key=request.session.session_key)
    web_user_queryset = WebUser.objects.filter(session=session)
    web_user = list(web_user_queryset)
    if web_user is not None and len(web_user) > 0:
        web_user = web_user[0]
        web_user.update()
    return HttpResponse(status=200)

def open_phone(request, device_id):
	pass

def close_phone(request, device_id):
	pass

def tap_phone(request, device_id):
	pass
