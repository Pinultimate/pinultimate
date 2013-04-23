from django.core.management.base import BaseCommand
from optparse import make_option
from heatmap.models import Location
from server.settings import DBNAME
import mongoengine as mongo
import random
import datetime

class LocationGenerator:
    def __init__(self, db_name, command):
        random.seed()
        self.command = command
        self.db_name = db_name
        mongo.connect(db_name)
        self.fake_locations = []

    #center is a dict with values for 'latitude' and 'longitude'. latrange and longrange are the
    #maximum distances from the center in the y and x directions, respectively, for adding points.
    def generate_locations(self, center, latrange, lonrange, time, num_locations):
        for i in range(num_locations):
            lon = center['longitude'] + (random.random() * lonrange * random.choice([1,-1]))
            lat = center['latitude'] + (random.random() * latrange * random.choice([1,-1]))
            self.fake_locations.append({"coords":{'latitude':lat,'longitude':lon}, "timestamp":time})

    def print_locations(self):
        for fake_location in self.fake_locations:
            self.stdout.write(fake_location)

    def add_locations_to_db(self):

        #connection = pymongo.Connection()
        #db = connection[self.db_name]
        #db_location = db.location
        for fake_location in self.fake_locations:
            fake_coords = fake_location['coords']
            fake_timestamp = fake_location['timestamp']
            location = Location(
                coordinates=[fake_coords['latitude'], fake_coords['longitude']],
                timestamp=fake_timestamp,
                time_added_to_db=datetime.datetime.now(),
            )
            location.save()
        self.command.stdout.write('%d fake_locations > %s' % (len(self.fake_locations), self.db_name))

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
            make_option('--lat',
                        type=float,
                        default=37.44,
                        help="latitude"
            ),
            make_option('--lon',
                        type=float,
                        default=-122.14,
                        help='longitude'
            ),
            make_option('--latrange',
                        type=float,
                        default=0.01,
                        help='maximum delta of latitude',
            ),
            make_option('--lonrange',
                        type=float,
                        default=0.02,
                        help='maximum delta of longitude'
            ),
            make_option('--num_per_hour',
                        type=int,
                        default=10,
                        help='num points per hour desired'
            ),
            make_option('--db_name',
                        type=str,
                        default=DBNAME,
                        help='db to store points in'
            ),
            make_option('--start_time',
                        type=str,
                        default='2000-1-1 0:0:0',
                        help='beginning time of the generated fake data'
            ),
            make_option('--num_hours',
                        type=int,
                        default=1,
                        help='number of hours to span'
            ),
            make_option('-p',
                        '--print',
                        dest='output_method',
                        action='store_const',
                        const=LocationGenerator.print_locations,
                        default=LocationGenerator.add_locations_to_db,
                        help='output to stdout rather than to database'
            )
        )

    def handle(self, *args, **options):
        #parser = argparse.ArgumentParser(description="Generate dummy data points (coords and timestamp) to populate db with.")
        #init_parse_args(parser)
        #args = parser.parse_args()

        gen = LocationGenerator(options['db_name'], self)
        center = {'latitude':options['lat'], 'longitude':options['lon']}
        t = datetime.datetime.strptime(options['start_time'],'%Y-%m-%d %H:%M:%S')

        for x in range(options['num_hours']):
            gen.generate_locations(center, options['latrange'], options['lonrange'], t + datetime.timedelta(hours=x), options['num_per_hour'])
        options['output_method'](gen)
