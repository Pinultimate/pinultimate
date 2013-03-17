from django.http import HttpResponse
from django.views.decorators.http import require_http_methods


VERIFICATION_TOKEN = 'geography'
SUBSCRIBE = 'subscribe'

@require_http_methods(['GET' 'POST'])
def subscription(request):
    if request.method == 'GET':
        return confirm_subscription(request.GET)
    elif request.method == 'POST':
        write_instagram_data_to_database(request.POST)
        return HttpResponse(status=200)

def confirm_subscription(args):
    if args['hub.verify_token'] != VERIFICATION_TOKEN:
        return HttpResponse(status=403)
    if args['hub.mode'] != SUBSCRIBE:
        return HttpResponse(status=403)

    return HttpResponse(args['hub.challenge'])

def write_instagram_data_to_database(args):
    # TODO: take post data and update it in MongoDB
    pass
