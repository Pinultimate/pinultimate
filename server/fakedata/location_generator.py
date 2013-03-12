import sys
import time
import random
import pymongo
import datetime
import argparse

'''This class is for populating the database with fake data points.'''

class LocationGenerator:

    def __init__(self, db_name):
        random.seed()
        self.db_name = db_name
        self.locations = []
        
    #center is a dict with values for 'latitude' and 'longitude'. latrange and longrange are the
    #maximum distances from the center in the y and x directions, respectively, for adding points.
    def generate_locations(self, center, latrange, lonrange, time, num_locations):
        for i in range(num_locations):
            lon = center['longitude'] + (random.random() * lonrange * random.choice([1,-1]))
            lat = center['latitude'] + (random.random() * latrange * random.choice([1,-1]))
            self.locations.append({"coords":{'latitude':lat,'longitude':lon}, "timestamp":time})

    def print_locations(self):
        for location in self.locations:
            print location

    def add_locations_to_db(self):
        connection = pymongo.Connection()
        db = connection[self.db_name]
        db_location = db.location
        for location in self.locations:
            db_location.insert(location)
        print 'Points stored in database'


def init_parse_args(parser):
    parser.add_argument('--lat', type=float, help="latitude", default=37.44)
    parser.add_argument('--lon', type=float, help='longitude', default=-122.14)
    parser.add_argument('--latrange', type=float, help='maximum delta of latitude', default=0.01)
    parser.add_argument('--lonrange', type=float, help='maximum delta of longitude', default=0.02)
    parser.add_argument('--num-per-hour', type=int, help='num points per hour desired', default=10)
    parser.add_argument('--db_name', type=str, help='db to store points in', default='HEATMAP_DB')
    parser.add_argument('-p', '--print', dest='output_method', action='store_const',
                        const=LocationGenerator.print_locations, default=LocationGenerator.add_locations_to_db,
                        help='output to stdout rather than to database')
    
def main():
    parser = argparse.ArgumentParser(description="Generate dummy data points (coords and timestamp) to populate db with.")
    init_parse_args(parser)
    args = parser.parse_args()

    gen = LocationGenerator(args.db_name)
    center = {'latitude':args.lat, 'longitude':args.lon}
    t = datetime.datetime.utcnow()

    for x in range(10):
        gen.generate_locations(center, args.latrange, args.lonrange, t - datetime.timedelta(hours=x), args.num_per_hour)
    args.output_method(gen)
    

if __name__ == '__main__':
    main()
