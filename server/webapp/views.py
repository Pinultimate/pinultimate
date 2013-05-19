from django.shortcuts import render_to_response
from django.contrib.sessions.models import Session
from django.http import HttpResponse
from models import WebUser
from datetime import datetime

CSS_M='text/css'
JS_M='text/javascript'
PNG_M='image/png'
JPG_M='image/jpeg'
WEBAPP_DIR='/home/deploy/pinultimate/frontend/standard_web/'
DATA_SUBDIR='resources/'

def index(request):
    if not request.session.exists(request.session.session_key):
        request.session.create()

    session = Session.objects.get(session_key=request.session.session_key)
    web_user_queryset = WebUser.objects.filter(session=session)
    web_user = list(web_user_queryset)
    if web_user is None or len(web_user) == 0:
        web_user = WebUser(session=session)
    else:
        web_user = web_user[0]
    web_user.total_visits += 1
    web_user.last_updated = datetime.now()
    web_user.save()

    return render_to_response('map.html')

def feedback_html(request):
    return render_to_response('feedback.html')

def style_css(request):
    return render_to_response(DATA_SUBDIR + 'style.css', mimetype=CSS_M)

def sample_data_js(request):
    return render_to_response(DATA_SUBDIR + 'sampleData.js', mimetype=JS_M)

def kmeans_js(request):
    return render_to_response(DATA_SUBDIR + 'KMeans.js', mimetype=JS_M)

def time_slider_js(request):
    return render_to_response(DATA_SUBDIR + 'time_slider.js', mimetype=JS_M)

def data_js(request):
    return render_to_response(DATA_SUBDIR + 'data.js', mimetype=JS_M)

def map_js(request):
    return render_to_response(DATA_SUBDIR + 'map.js', mimetype=JS_M)

def white_wall_hash_png(request):
    image_data = open(WEBAPP_DIR + DATA_SUBDIR + "white_wall_hash.png", "rb").read()
    return HttpResponse(image_data, mimetype=PNG_M)

def pause_button_jpeg(request):
    image_data = open(WEBAPP_DIR + DATA_SUBDIR + "PauseButton.jpeg", "rb").read()
    return HttpResponse(image_data, mimetype=JPG_M)

def play_button_jpeg(request):
    image_data = open(WEBAPP_DIR + DATA_SUBDIR + "PlayButton.jpeg", "rb").read()
    return HttpResponse(image_data, mimetype=JPG_M)
