#!/bin/bash

curl -F 'client_id=f6667e2778b84c5499a5fe4f8e207757' \
	-F 'client_secret=3a299b864af941de9158d2e1f6a2fcce' \
	-F 'object=geography' \
	-F 'aspect=media' \
	-F 'lat=37.4419' \
	-F 'lng=-122.1419' \
	-F 'radius=5000' \
	-F 'verify_token=geography' \
	-F 'callback_url=http://api.pinultimate.net/instagram/subscription/' \
	https://api.instagram.com/v1/subscriptions/
