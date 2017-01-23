WordPress meetup scraper
========================

This is a simple tool that uses the meetup.com and central.wordcamp.org api to
aggregate WordPress events. An api key for meetup.com is required to use this
tool, that can be obtained by creating an account on meetup.com and visiting
https://secure.meetup.com/meetup_api/key/ , note that this is a private key
tied to your account, do not share it.

Use:

.. code-block:: console

    ./scraper.py $meetup_key

to get
a list of WordCamps and WordPress meetups in json format. The json can then be
used to create calendar events or used in websites to list upcoming events.

.. code-block:: console

    ./scraper.py $meetup_key | jq '.' | less

for nice output on linux.

This came about as a result of discussions held in
https://make.wordpress.org/hosting/2017/01/18/hosting-meeting-notes-january-18-2017/
. It is part of an effort to encourage attendance of WordPress events.
