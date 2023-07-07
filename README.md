# helium-reader

This is an older demo that worked with tracking helium before it was subsumed into Solana. 

The purpose of the the demo originally was to allow a group to have logins, then when logged in, hotspots they wanted tracked could be added. Once the hotspot was added, the last 60 days of rewards for it were automatically picked up, then moving forward new rewards were added once a day.

I set it up in a Docker container using docker-compose, and used Django to set up the project. I used selenium, celery, flower, postgres, pandas, numpy, django-cors-headers, etc.

The commands for tasks like getting the last 60 days of hnt rewards per hotspot from the api can be found following this path:

apps/hotspots/management/commands

The helium_sixty.py command is called when a hotspot view is created. That call can be seen in apps/hotspots/views.py and is called HotspotCreateView. The other command is called once a day and makes sure it doesn't add in rewards that are already there. It is called via celery beat in hr_projects/celery.py
