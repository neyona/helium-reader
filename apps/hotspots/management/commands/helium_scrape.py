import os
import json
import datetime
import pandas as pd
import numpy as np
from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from urllib.request import urlopen
from django.utils import timezone, dateparse

from apps.rewards.models import Reward
from apps.hotspots.models import Hotspot
from apps.hotspots.serializers import HotspotSerializer

# to run a command, run docker-compose exec web python3 manage.py then the
# add the name of the file minus the .py. The command is the name of the file.
# Commands have to be in a management/commands/ directories
# get and make the URL beforehand so then the command is called by the hotspot


class Command(BaseCommand):
    help = 'Helium daily rewards'
    # Command logic

    def handle(self, *args, **kwargs):
        time = timezone.now().strftime('%X')
        print_date = datetime.date.today().strftime('%Y-%m-%d')
        string_print_date = str(print_date)
        current_date = datetime.datetime.now()
        current_date = current_date.\
            replace(tzinfo=datetime.timezone.utc)
        """Technically this is skilled and run farther down. """

        def daily_scrape(hotspot):
            print_date = datetime.date.today().strftime('%Y-%m-%d')
            string_print_date = str(print_date)
            current_date = datetime.datetime.now()
            current_date = current_date.\
                replace(tzinfo=datetime.timezone.utc)
            hotspot_name = hotspot.hotspot_name
            location_url = hotspot.location_url
            hotspot_id = hotspot.id
            hotspot = Hotspot.objects.filter(id=hotspot_id)
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            driver = webdriver.Chrome(chrome_options=chrome_options)
            beginning_url = 'https://helium-api.stakejoy.com/v1/hotspots/' + location_url + '/'
            url_end = 'rewards/sum?min_time=-14%20day&max_time={}T00%3A00%3A00.000Z&bucket=day'.format(
                string_print_date)
            check_url = beginning_url + url_end
            driver.get(check_url)
            check_json = json.loads(driver.find_element(By.TAG_NAME, "pre").text)
            jsonString = json.dumps(check_json)
            jsonFile = open("jsonfiles/data.json", "w")
            jsonFile.write(jsonString)
            jsonFile.close()
            df = pd.json_normalize(check_json, record_path=['data'])

            def tr_func(x):
                new_date = x.split('T')[0]
                return new_date

            df = pd.DataFrame(df, columns=['timestamp', 'sum']).head(7)
            df['timestamp'] = df['timestamp'].apply(tr_func)
            hotspot_check = SelDB.objects.filter(hotspot__hotspot_name=hotspot_name)

            def check_date(ts):
                # this is to make sure that the data doesn't already exist
                check_date = hotspot_check.filter(timestamp=ts)
                if check_date.exists():
                    return True
                else:
                    return False

            df.insert(0, 'hotspot', hotspot_name)
            df.drop(df[df['timestamp'].apply(check_date) == True].index, inplace=True)
            df.insert(0, 'Date Added', current_date)
            df.insert(4, 'comment', '')
            row_iter = df.iterrows()
            objs = [
                Reward(
                    hotspot_id=row['hotspot'],
                    date_celery_added_instance_to_database=row['Date Added'],
                    timestamp=row['timestamp'],
                    sum=row['sum'],
                    comment_in_case_of_change=row['comment']
                )
                for index, row in row_iter
            ]
            Reward.objects.bulk_create(objs)
            with open("jsonfiles/data.json", "r+") as f:
                f.truncate(0)
            driver.quit()

        """This is where the command actually starts. It runs the daily_scrape."""
        hotspot_set = Hotspot.objects.all()
        for hotspot in hotspot_set.iterator():
            daily_scrape(hotspot)
