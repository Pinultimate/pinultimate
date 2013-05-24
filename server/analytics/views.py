from webapp.models import WebUser
from analytics.models import PhoneUser
from django.contrib.sessions.models import Session
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext

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

@csrf_exempt
@require_POST
def open_phone(request, device_id):
	phone_user_queryset = PhoneUser.objects.filter(phone_id=device_id)
	phone_user = list(phone_user_queryset)
	if phone_user is not None and len(phone_user) > 0:
		phone_user = phone_user[0]
		phone_user.open_app()
	else:
		phone_user = PhoneUser(phone_id=device_id)
		phone_user.total_visits += 1
		phone_user.save()

	return HttpResponse(status=200)

@csrf_exempt
@require_POST
def close_phone(request, device_id):
	phone_user_queryset = PhoneUser.objects.filter(phone_id=device_id)
	phone_user = list(phone_user_queryset)
	if phone_user is not None and len(phone_user) > 0:
		phone_user = phone_user[0]
		phone_user.close_app()

	return HttpResponse(status=200)

@csrf_exempt
@require_POST
def tap_phone(request, device_id):
	phone_user_queryset = PhoneUser.objects.filter(phone_id=device_id)
	phone_user = list(phone_user_queryset)
	if phone_user is not None and len(phone_user) > 0:
		phone_user = phone_user[0]
		phone_user.tap()

	return HttpResponse(status=200)


def user_analytics_page(request):
    num_users_web = WebUser.objects.filter().count()
    num_users_mobile = PhoneUser.objects.filter().count()
    avg_visits_web = "{0:.2f}".format(WebUser.objects.raw('select id, avg(total_visits) as avg from webapp_webuser')[0].avg)
    avg_visits_mobile = "{0:.2f}".format(PhoneUser.objects.raw('select id, avg(total_visits) as avg from analytics_phoneuser')[0].avg)
    avg_taps_web = "{0:.2f}".format(WebUser.objects.raw('select id, avg(total_taps) as avg from webapp_webuser')[0].avg)
    avg_taps_mobile = "{0:.2f}".format(PhoneUser.objects.raw('select id, avg(total_taps) as avg from analytics_phoneuser')[0].avg)
    avg_seconds_web = WebUser.objects.raw('select id, avg(total_seconds_spent) as avg from webapp_webuser')[0].avg
    avg_min_web = "{0:.2f}".format(float(avg_seconds_web)/60)
    avg_seconds_mobile = PhoneUser.objects.raw('select id, avg(total_seconds_spent) as avg from analytics_phoneuser')[0].avg
    avg_min_mobile = "{0:.2f}".format(float(avg_seconds_mobile)/60)
    num_return_users_web = WebUser.objects.filter(total_visits__gt=1).count()
    ret_rate_web = "{0:.2f}%".format((float(num_return_users_web)/num_users_web)*100)
    num_return_users_mobile = PhoneUser.objects.filter(total_visits__gt=1).count()
    ret_rate_mobile = "{0:.2f}%".format((float(num_return_users_mobile)/num_users_mobile)*100)

    data = {
        'total_num_users_web' : num_users_web,
        'total_num_users_mobile' : num_users_mobile,
        'avg_num_visits_web' : avg_visits_web,
        'avg_num_visits_mobile' : avg_visits_mobile,
        'avg_num_taps_web' : avg_taps_web,
        'avg_num_taps_mobile' : avg_taps_mobile,
        'avg_time_web' : str(avg_min_web) + " minutes",
        'avg_time_mobile' : str(avg_min_mobile) + " minutes",
        'return_rate_web' : ret_rate_web,
        'return_rate_mobile' : ret_rate_mobile,
        }
    return render_to_response('user_analytics.html', data, context_instance=RequestContext(request))
