from normalize import *
import os
import json
import sys


test_data =[{"latitude": 40, "longitude": -121, "value": 2}, {"latitude": 38, "longitude": -123, "value": 3}]
def main(argv):
    test = Normalize(test_data)
    #test.normValue()
    test.densityToValue()
    #test.valueToDensity()
    #test.normDensity()
    print test.data

if __name__ == '__main__':
    main(sys.argv)
