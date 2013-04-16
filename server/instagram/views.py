from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
import hmac
import hashlib
from django.views.decorators.csrf import csrf_exempt
from django.core.management import call_command

FILESPATH = '/home/deploy/pinultimate/server/instagram/files/'

VERIFICATION_TOKEN = 'geography'
SUBSCRIBE = 'subscribe'

CLIENT_ID = 'f6667e2778b84c5499a5fe4f8e207757'
CLIENT_SECRET = '3a299b864af941de9158d2e1f6a2fcce'


@csrf_exempt
@require_http_methods(['GET','POST'])
def subscription(request):
    if request.method == 'GET':
        return confirm_subscription(request.GET)
    elif request.method == 'POST':
        write_instagram_data_to_database(request)
        return HttpResponse(status=200)

def confirm_subscription(args):
    if args['hub.verify_token'] != VERIFICATION_TOKEN:
        return HttpResponse(status=403)
    if args['hub.mode'] != SUBSCRIBE:
        return HttpResponse(status=403)

    return HttpResponse(args['hub.challenge'])

def write_instagram_data_to_database(request):
    # TODO: take post data and update it in MongoDB, write json data to a file
    # for now
    
    json_string = str(request.body)
    call_command('handleIG', json_string, CLIENT_ID)

    if not verify_signature(CLIENT_SECRET, request.body,
            request.META['HTTP_X_HUB_SIGNATURE']):
        raise ValidationError("X-Hub-Signature and hmac digest did not match")

def verify_signature(client_secret, raw_response, x_hub_signature):
    digest = hmac.new(client_secret.encode('utf-8'),
                      msg=raw_response.encode('utf-8'),
                      digestmod=hashlib.sha1
                      ).hexdigest()
    return digest == x_hub_signature
