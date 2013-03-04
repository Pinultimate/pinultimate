# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Command-line skeleton application for Google+ API.
Usage:
  $ python gplus_scraper.py

You can also get help on all the command-line flags the program understands
by running:

  $ python gplus_scraper.py --help

To get detailed log output run:

  $ python gplus_scraper.py --logging_level=DEBUG
"""

import gflags
import httplib2
import logging
import os
import pprint
import sys
import json

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run


FLAGS = gflags.FLAGS

# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret.
# You can see the Client ID and Client secret on the API Access tab on the
# Google APIs Console <https://code.google.com/apis/console>
CLIENT_SECRETS = 'client_secrets.json'

# Helpful message to display if the CLIENT_SECRETS file is missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this application run you will need to download the client_secrets.json file
and save it at:

   %s

""" % os.path.join(os.path.dirname(__file__), CLIENT_SECRETS)

# Set up a Flow object to be used for authentication.
# Add one or more of the following scopes. PLEASE ONLY ADD THE SCOPES YOU
# NEED. For more information on using scopes please see
# <https://developers.google.com/+/best-practices>.
FLOW = flow_from_clientsecrets(CLIENT_SECRETS,
    scope=[
      'https://www.googleapis.com/auth/plus.login',
      'https://www.googleapis.com/auth/plus.me',
    ],
    message=MISSING_CLIENT_SECRETS_MESSAGE)


# The gflags module makes defining command-line options easy for
# applications. Run this program with the '--help' argument to see
# all the flags that it understands.
gflags.DEFINE_enum('logging_level', 'ERROR',
    ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
    'Set the level of logging detail.')


def main(argv):
  # Let the gflags module process the command-line arguments
  try:
    argv = FLAGS(argv)
  except gflags.FlagsError, e:
    print '%s\\nUsage: %s ARGS\\n%s' % (e, argv[0], FLAGS)
    sys.exit(1)

  # Set the logging according to the command-line flag
  logging.getLogger().setLevel(getattr(logging, FLAGS.logging_level))

  # If the Credentials don't exist or are invalid, run through the native
  # client flow. The Storage object will ensure that if successful the good
  # Credentials will get written back to a file.
  storage = Storage('gplus_scraper.dat')
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run(FLOW, storage)

  # Create an httplib2.Http object to handle our HTTP requests and authorize it
  # with our good Credentials.
  http = httplib2.Http()
  http = credentials.authorize(http)

  service = build('plus', 'v1', http=http)

  try:

    activities_resource = service.activities()    
    activities_count = 0
    geo_activities_count = 0
    geo_info = []
    activities_document = None

    print 'Scraping Public Activities for Geo Info ... '
    while activities_document == None or 'nextPageToken' in activities_document:
      page_token = None
      if activities_document != None:
        page_token = activities_document['nextPageToken']
      
      activities_document = activities_resource.search(query='', maxResults=None, orderBy=None, pageToken=page_token).execute()
      for activity in activities_document['items']:
        activities_count += 1
        if 'geocode' in activity:
          geo_activities_count += 1
          geo_info.append(activity)
          print '!Found an activity with GEO Info! Currently has %d' % geo_activities_count
        if activities_count % 100 == 0:
          print 'Scraped %d public activities, continuing ...' % activities_count

    # For more information on the Google+ API API you can visit:
    #
    #   https://developers.google.com/+/api/
    #
    # For more information on the Google+ API API python library surface you
    # can visit:
    #
    #   https://google-api-client-libraries.appspot.com/documentation/plus/v1/python/latest/
    #
    # For information on the Python Client Library visit:
    #
    #   https://developers.google.com/api-client-library/python/start/get_started

  except AccessTokenRefreshError:
    print ("The credentials have been revoked or expired, please re-run"
      "the application to re-authorize")

if __name__ == '__main__':
  main(sys.argv)
