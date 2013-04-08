from normalize import *
from merge import *
from grid_mapping import *
import os
import json
import sys


test_data =[{"latitude": 40, "longitude": -121, "value": 2}, {"latitude": 38, "longitude": -123, "value": 3}]
test_data1 =[{"latitude": 37, "longitude": -121}, {"latitude": 38, "longitude": -123}]

def main(argv):
    #test = Normalize(test_data)
    #test.normValue()
    #test.densityToValue()
    #test.valueToDensity()
    #test.normDensity()
    #test = Merge()
    #test.addData(test_data, 10)
    #test.addData(test_data1, 5)
    #test.valueBasedMerege()
    #test.densityBasedMerge()
    test = Grid_mapping()
    print test.gridify(-175, 85, 10)
    print test.gridify(-165, 85, 10)
    print test.gridify(0, 0, 10)


    print test.grid_center(0, 0, 10)
    print test.grid_center(1, 0, 10)
    print test.grid_center(0, 1, 10)
    print test.grid_center(1, 1, 10)

    


if __name__ == '__main__':
    main(sys.argv)
