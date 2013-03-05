#!/usr/bin/python

import facebook
from pprint import pprint

access_token = graph = "AAAAAAITEghMBAAXTQH21HAM7pJXJtDInA0ZC8neaIyy7DdHYEAlTqijg2cqBrZCATXwgc5sw07ZBs2HIjEqQoIHinFkjAJELnlX3AEEDmF0rrtDV5Uh"

def scrape():
    graph = facebook.GraphAPI(access_token)
    checkins = graph.get_object("search", type="checkin")['data']
    for elem in checkins:
        pprint(elem['place'])

if __name__ == "__main__":
    scrape()
