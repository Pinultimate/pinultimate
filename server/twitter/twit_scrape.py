from twitter import *

OAUTH_TOKEN = '1373732868-rJSi4IAzTh5ruvimgs4NxsrZUtOOgKT8LLceeU'
OAUTH_SECRET = 'LtPxpNbsiy5tWgMd1SfEaEvt0NPlkXvRH3ky1hkovw'
CONSUMER_KEY = 'A7R0OmDF2kJvdIwHkYaSaA'
CONSUMER_SECRET = 'FDFfHcKyr2vxa33qMghDPETi2CfztsxC9LPVNyJe0'

#LAT1 = 36.9419
#LAT2 = 37.9419
#LON1 = -121.1419
#LON2 = -122.6419
LON1, LAT1, LON2, LAT2 = (-122.75,36.8,-121.75,37.8)

locations_args = "%f,%f,%f,%f" % (LON1, LAT1, LON2, LAT2)

def write_to_db(json_data):
    #make sure to count all pics by the same user in one hour as one 'checkin'
    for elem in json_data:
        date_taken = int(time.mktime(time.strptime(elem['datetaken'], "%Y-%m-%d %H:%M:%S")))
        location = FlickrLocation(
            coordinates = [elem['latitude'], elem['longitude']],
            timestamp = date_taken,
            user_id = elem['ownername'],
        )
        location.save()

def main():
    twitter_stream = TwitterStream(
            auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET,
                       CONSUMER_KEY, CONSUMER_SECRET)
           )
    #iterator = twitter_stream.statuses.filter(locations="-121.1419,36.9419,-122.6419,37.9419")
    iterator = twitter_stream.statuses.filter(locations=locations_args)
    for tweet in iterator:
        print tweet


if __name__ == '__main__':
    main()
