from webapp.models import WebUser
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@require_POST
def tap(request):
    web_user = WebUser.objects.get(session=request.session)
    if web_user is not None:
        web_user.tap()
    return HttpResponse(status=200)


@csrf_exempt
@require_POST
def update(request):
    web_user = WebUser.objects.get(session=request.session)
    if web_user is not None:
        web_user.update()
    return HttpResponse(status=200)