import sys
import time
import random
import pymongo
import datetime

'''
This class is for populating the database with fake data points.
'''

class PointGenerator:

    def __init__(self):
        self.points = []
        random.seed()
    
    #center is a dict with values for 'latitude' and 'longitude'. xrange
    #is how far from the center in the x direction that points can be.
    #same for yrange. time and num_points are self-explanatory
    def generate_points(self, center, xrange, yrange, time, num_points):
        for i in range(num_points):
            long = center['longitude'] + random.random()*xrange
            lat = center['latitude'] + random.random()*yrange
            self.points.append({"coords":{'latitude':lat,'longitude':long}, "timestamp":time})

    def print_points(self):
        for point in self.points:
            print point

    def add_to_db(self, db_name):
        connection = pymongo.Connection()
        db = connection[db_name]
        points = db.points
        for point in self.points:
            points.insert(point)


SEC_IN_HOUR = 3600
            
def main(args):
    center = {'latitude':37.44,'longitude':-122.14}
    gen = PointGenerator()
    t = datetime.datetime.utcnow()
    for i in range(10):
        gen.generate_points(center, 0.02, 0.01, t - datetime.timedelta(hours=i), 10)
    #gen.print_points()
    gen.add_to_db('dummy_data')
    
'''
def usage(program_name):
    print 'Usage: '
    print '  python ' + program_name + ' [latitude] [longitude] [latrange] [longrange] [num_per_hour]'
'''
    
if __name__ == '__main__':
    args = sys.argv
    main(args)
