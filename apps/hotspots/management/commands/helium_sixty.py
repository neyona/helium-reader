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
    help = 'helium first sixty reward instances after sign up'
    # Command logic

    def add_arguments(self, parser):
        parser.add_argument(
            'hotspot_id',
            type=str,
            help='The new hotspot_id should be passed with the call_command'
        )

    def handle(self, *args, **kwargs):
        # a test
        time = timezone.now().strftime('%X')
        self.stdout.write("It is now %s" % time)
        print_date = datetime.date.today().strftime('%Y-%m-%d')
        self.stdout.write("The date is now %s" % print_date)
        string_print_date = str(print_date)
        current_date = datetime.datetime.now()
        # Replacing the value of the timezone in tzinfo class of
        # the object using the replace() function
        hotspot_id = kwargs['hotspot_id']
        print(hotspot_id)
        current_date = current_date.\
            replace(tzinfo=datetime.timezone.utc)
        # Converting the date value into ISO 8601
        # format using isoformat() method
        current_date = current_date.isoformat()
        hotspot = Hotspot.objects.filter(id=hotspot_id)
        hotspot_list = str(hotspot[0]).split(',')
        hotspot_name = hotspot_list[0]
        location_url = hotspot_list[1]
        print('Selenium Chrome opening ..')
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        print("space left to help me find out what's happening")
        beginning_url = 'https://helium-api.stakejoy.com/v1/hotspots/' + location_url + '/'
        url_end = 'rewards/sum?min_time=-60%20day&max_time={}T00%3A00%3A00.000Z&bucket=day'.format(
            string_print_date)
        check_url = beginning_url + url_end
        driver.get(check_url)
        """
        current url is and attribute, not a variable
        """
        print(driver.current_url)
        """
        The next part is in python data format as well and is also a dictionary.
        It contains all the scraped data.
        """
        check_json = json.loads(driver.find_element(By.TAG_NAME, "pre").text)
        jsonString = json.dumps(check_json)
        jsonFile = open("jsonfiles/sixdata.json", "w")
        jsonFile.write(jsonString)
        jsonFile.close()
        print("adding in pandas")
        """
        normalizes the data, but I cannot perform all actions here. It is also
        ALL of the data, more than I need. It puts it into a Dataframe.
        """
        df = pd.json_normalize(check_json, record_path=['data'])
        print(df.to_string())

        def tr_func(x):
            new_date = x.split('T')[0]
            return new_date
        df = pd.DataFrame(df, columns=['timestamp', 'sum'])
        print(df)
        """
        The next line returned the DataFrame with the transformed timestamp.
        I changed it to update the dataframe so I wouldn't have extra dataframes
        in memory.
        """
        df['timestamp'] = df['timestamp'].apply(tr_func)
        df.insert(0, 'Date Added', current_date)
        df.insert(0, 'hotspot', hotspot_name)
        df.insert(4, 'comment', '')
        print(df)
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
        with open("jsonfiles/sixdata.json", "r+") as f:
            f.truncate(0)
        driver.quit()
