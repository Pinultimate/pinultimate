from django.shortcuts import render_to_response
from django.http import HttpResponse
from models import WebUser
from datetime import datetime

CSS_M='text/css'
JS_M='text/javascript'
PNG_M='image/png'
WEBAPP_DIR='/home/deploy/pinultimate/frontend/standard_web/'
DATA_SUBDIR='resources/'

def index(request):
    web_user = WebUser.objects.get(session=request.session)
    if web_user is not None:
        web_user = WebUser(session=request.session)
    web_user.total_visits += 1
    web_user.last_updated = datetime.now()
    web_user.save()

    return render_to_response('map.html')

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

