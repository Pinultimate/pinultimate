from django.core.management.base import BaseCommand
import datetime
from metrics.models import Location
import mongoengine as mongo
from server.settings import DBNAME


def main(num_days):
    today = datetime.datetime.now()
    today -= datetime.timedelta(0, today.second, today.microsecond, 0, today.minute, today.hour, 0)
    delta = datetime.timedelta(1)
    
    print "Printing num photos downloaded per day for the past " + str(num_days) + " days:"

    instagram_total = 0
    flickr_total = 0
    for i in range(num_days):
        print "  " + (today - datetime.timedelta(i)).strftime("%D")
        instagram_entries = Location.objects(timestamp__lte=today+delta, timestamp__gte=today, source="instagram")
        instagram_total += len(instagram_entries)
        print "    Instagram: " + len(instagram_entries)
        flickr_entries = Location.objects(timestamp__lte=today+delta, timestamp__gte=today, source="flickr")
        flickr_total += len(flickr_entries)
        print "    Flickr: " + len(flickr_entries)

    print "\nTotals for past " + str(num_days) + " days:"
    print "  Instagram: " + instagram_total
    print "  Flickr: " + flickr_total

class Command(BaseCommand):
    def handle(self, *args, **options):
        mongo.connect(DBNAME)
        num_days = 5
        if len(args) > 0:
            try:
                num_days = int(args[0])
            except ValueError:
                pass
        main(num_days)
