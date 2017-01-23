#!/usr/bin/python3

from __future__ import print_function
import requests
import json
import datetime
import sys

meetup_key = sys.argv[1]

event_list = list()

r = requests.get('https://central.wordcamp.org/wp-json/posts?type=wordcamp&filter[posts_per_page]=100',
        verify=False)
json_response = r.json()
for i in json_response:
    for j in i['post_meta']:
        if j['key'] == 'Location':
            location = j['value']

        if j['key'] == 'WordCamp Hashtag':
            hashtag = j['value']

        if j['key'] == 'Twitter':
            twitter = j['value']

        if j['key'] == 'URL':
            url = j['value']

        if j['key'] == 'Start Date (YYYY-mm-dd)':
            start_date = int(j['value'])

        if j['key'] == 'End Date (YYYY-mm-dd)':
            end_date = j['value']
            if end_date:
                end_date = int(end_date)

    status = i['status']
    title = i['title']

    if status == "wcpt-scheduled":
        #print(title, ",", url, ",", twitter, ",", start_date, ",", end_date, ",",location, ",", hashtag)
        event = {
            "title": title,
            "url": url,
            "twitter": twitter,
            "start": start_date,
            "end": end_date,
            "location": location,
            "hashtag": hashtag
            }
        event_list.append(event)

r = requests.get('https://api.meetup.com/2/events?member_id=72560962&key=%s&sign=true' % meetup_key)

json_response = r.json()
for i in json_response['results']:
    title = i['group']['name']
    url = i['event_url']
    start_date = int(i['time'])/1000
    if 'venue' in i.keys():
        location = i['venue']['city'] + ", " + i['venue']['localized_country_name']
    else:
        location = None

    #print(title, ",", url, ",", start_date)
    event = {
        "title": title,
        "url": url,
        "twitter": None,
        "start": start_date,
        "end": None,
        "location": location,
        "hashtag": None
        }
    event_list.append(event)

print(json.dumps(event_list))
