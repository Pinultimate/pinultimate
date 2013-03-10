from django.http import HttpResponse

# Create your views here.
def find_locations(request, latitude, longitude, year, month, day, hour, minute):
	return HttpResponse("Latitude : %s\nLongitude : %s\nDatetime : %s/%s/%s, %s:%s" % (latitude, longitude, month, day, year, hour, minute))

def find_all_locations(request, latitude, longitude):
	return HttpResponse("Latitude : %s\nLongitude : %s" % (latitude, longitude))