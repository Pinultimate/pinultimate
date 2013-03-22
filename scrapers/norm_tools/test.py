from normalize import *
from merge import *
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
    test = Merge()
    test.addData(test_data, 10)
    test.addData(test_data1, 5)
    #test.valueBasedMerege()
    test.densityBasedMerge()
    print test.data

if __name__ == '__main__':
    main(sys.argv)
