#!/usr/bin/python3

from __future__ import print_function
import requests
import json
import datetime
import sys
import zipcode

meetup_key = sys.argv[1]

event_list = list()

r = requests.get('https://central.wordcamp.org/wp-json/posts?type=wordcamp&filter[posts_per_page]=100',
        verify=False)
json_response = r.json()
for i in json_response:
    # loop through the dicts in "post_meta" to find the data we need
    for j in i['post_meta']:

        # Grab the location
        if j['key'] == 'Location':
            location = j['value']

        # Grab the official hashtag
        if j['key'] == 'WordCamp Hashtag':
            hashtag = j['value']

        # Grab the official twitter handle
        if j['key'] == 'Twitter':
            twitter = j['value']

        # Grab the url for the WordCamp website
        if j['key'] == 'URL':
            url = j['value']

        # Grab the start date, note the key says (YYY-mm-dd) but it is really a
        # Unix timestamp
        if j['key'] == 'Start Date (YYYY-mm-dd)':
            start_date = int(j['value'])

        # Grab the end date, note the key says (YYY-mm-dd) but it is really a
        # Unix timestamp
        if j['key'] == 'End Date (YYYY-mm-dd)':
            end_date = j['value']

            # If it exists set convert it to an int, it will sometimes be None
            if end_date:
                end_date = int(end_date)

    # Grab the status and timeline
    status = i['status']
    title = i['title']

    # If status is "wcpt-scheduled" it is an upcoming event
    if status == "wcpt-scheduled":
        event = {
            "title": title,
            "url": url,
            "twitter": twitter,
            "start": start_date,
            "end": end_date,
            "location": location,
            "hashtag": hashtag,
            "zipcode": None
            }
        event_list.append(event)

r = requests.get('https://api.meetup.com/2/events?member_id=72560962&key=%s&sign=true' % meetup_key)

json_response = r.json()
for i in json_response['results']:

    # Get the meetup name
    title = i['group']['name']

    # Get the event website url
    url = i['event_url']

    # Get the start time of the event, it is a unix timestamp*1000
    start_date = int(i['time'])/1000

    # If a venue is available get it
    if 'venue' in i.keys():
        location = i['venue']['city'] + ", " + i['venue']['localized_country_name']
        zip = None
        lat = None
        lon = None
        if "lat" in i['venue'].keys() and "lon" in i['venue'].keys():
            lat = i['venue']['lat']
            lon = i['venue']['lon']

        if 'zipcode' in i['venue'].keys():
            zip = i['venue']['zipcode']

        elif lat and lon:
            zipcodes = zipcode.isinradius((lat, lon), 1)
            if len(zipcodes) >= 1:
                zip = zipcodes[0]
                zip = zip.to_dict()['zip']
                print("doing the thing")

    else:
        location = None

    # Output in the same format as the WordCamps for consistency
    event = {
        "title": title,
        "url": url,
        "twitter": None,
        "start": start_date,
        "end": None,
        "location": location,
        "hashtag": None,
        'lat': lat,
        'lon': lon,
        "zipcode": zip
        }
    event_list.append(event)

#print(json.dumps(event_list))
