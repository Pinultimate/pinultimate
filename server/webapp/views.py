from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from models import WebUser

CSS_M='text/css'
JS_M='text/javascript'
PNG_M='image/png'
WEBAPP_DIR='/home/deploy/pinultimate/frontend/standard_web/'
DATA_SUBDIR='resources/'

def user_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            web_user = WebUser.objects.get(user=user)
            web_user.total_logins += 1
            web_user.save()
            login(request, user)
            # TODO: Redirect to a success page.
        #else:
            # Return a 'disabled account' error message
    #else:
        # Return an 'invalid login' error message.

def user_logout(request):
    logout(request)
    # TODO: Redirect to login page.

def user_register(request):
    pass

#TODO figure out redirect url
@login_required()
def index(request):
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

