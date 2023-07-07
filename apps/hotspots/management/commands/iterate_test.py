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


class Command(BaseCommand):
    help = 'Iteration test'
    # Command logic

    def handle(self, *args, **kwargs):
        # a test
        time = timezone.now().strftime('%X')
        self.stdout.write("It is now %s" % time)
        print_date = datetime.date.today().strftime('%Y-%m-%d')
        self.stdout.write("The date is now %s" % print_date)
        string_print_date = str(print_date)
        current_date = datetime.datetime.now()
        current_date = current_date.\
            replace(tzinfo=datetime.timezone.utc)
        """Technically this is skipped and run farther down. """

        def daily_scrape(hotspot):
            print_date = datetime.date.today().strftime('%Y-%m-%d')
            string_print_date = str(print_date)
            current_date = datetime.datetime.now()
            current_date = current_date.\
                replace(tzinfo=datetime.timezone.utc)
            hotspot_name = hotspot.hotspot_name
            location_url = hotspot.location_url
            hotspot_id = hotspot.id
            print(location_url)
            print(hotspot_name)
            print(hotspot_id)
            hotspot = Hotspot.objects.filter(id=hotspot_id)
            print('Selenium Chrome opening ..')
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
            print(driver.current_url)
            beginning_url = 'https://helium-api.stakejoy.com/v1/hotspots/' + location_url + '/'
            url_end = 'rewards/sum?min_time=-14%20day&max_time={}T00%3A00%3A00.000Z&bucket=day'.format(
                string_print_date)
            check_url = beginning_url + url_end
            driver.get(check_url)
            print(driver.current_url)
            check_json = json.loads(driver.find_element(By.TAG_NAME, "pre").text)
            jsonString = json.dumps(check_json)
            jsonFile = open("jsonfiles/data.json", "w")
            jsonFile.write(jsonString)
            jsonFile.close()
            print("json file should have closed")
            print("starting Pandas")
            df = pd.json_normalize(check_json, record_path=['data'])
            print("First Dataframe check - normalized json dataframe")
            print(df)

            def tr_func(x):
                new_date = x.split('T')[0]
                return new_date

            df = pd.DataFrame(df, columns=['timestamp', 'sum']).head(7)
            print("Second Dataframe check - timestamp and sum")
            print(df)
            df['timestamp'] = df['timestamp'].apply(tr_func)
            print("Third Dataframe check - changed to remove time from timestamp")
            print(df)
            hotspot_check = Reward.objects.filter(hotspot__hotspot_name=hotspot_name)

            def check_date(ts):
                # this is to make sure that the data doesn't already exist
                # hotspot_check = SelDB.objects.filter(hotspot__hotspot_name=hotspot_name)
                check_date = hotspot_check.filter(timestamp=ts)
                # check_date = SelDB.objects.filter(timestamp=ts)
                if check_date.exists():
                    return True
                else:
                    return False

            df.insert(0, 'hotspot', hotspot_name)
            print("Fourth Dataframe check - inserted the hotspot name")
            print(df)
            print("Am I empty? ", df.empty)
            # df[ (df['Marks'] == 100) & (df['Marks']>98) ].index
            # df.drop( df[(df['timestamp'].apply(check_date) == True) & (df['hotspot_name']=='hotspot.hotspot_name')].index, inplace=True)
            df.drop(df[df['timestamp'].apply(check_date) == True].index, inplace=True)
            print("Fifth Dataframe check - after the drop example")
            print(df)
            print("Am I empty? ", df.empty)
            print('Number of columns in Dataframe : ', len(df.columns))
            print('Number of rows in Dataframe : ', len(df.index))
            df.insert(0, 'Date Added', current_date)
            print("Sixth Dataframe check - the date this reward was added to the database")
            print(df)
            df.insert(4, 'comment', '')
            print("Seventh Dataframe check - comment column added, will iterrow next")
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
            with open("jsonfiles/data.json", "r+") as f:
                f.truncate(0)
            driver.close()
        #
        """This is where the command actually starts. It runs the daily_scrape."""
        hotspot_set = Hotspot.objects.all()
        print(hotspot_set)
        for hotspot in hotspot_set.iterator():
            print(hotspot.hotspot_name)
            print(hotspot.id)
            print(hotspot.location_url)
            daily_scrape(hotspot)




# https://helium-api.stakejoy.com/v1/hotspots/11dRze1EH8Gbs4WdFiRneSzMwjKAjhMAUPh8w4jt6qaWQVtoLRE/rewards/sum?min_time=-60%20day&max_time=2023-02-01T00%3A00%3A00.000Z&bucket=day
# https://helium-api.stakejoy.com/v1/hotspots/11dRze1EH8Gbs4WdFiRneSzMwjKAjhMAUPh8w4jt6qaWQVtoLRE/rewards/sum?min_time=-14%20day&max_time=2023-02-01T00%3A00%3A00.000Z&bucket=day
