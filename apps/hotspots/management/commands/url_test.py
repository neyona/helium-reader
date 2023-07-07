import os
import json
import datetime
from django.core.management.base import BaseCommand
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from django.utils import timezone, dateparse

from apps.rewards.models import Reward
from apps.hotspots.models import Hotspot
from apps.hotspots.serializers import HotspotSerializer


class Command(BaseCommand):
    help = 'helium testing'
    # Command logic

    def handle(self, *args, **kwargs):
        time = timezone.now().strftime('%X')
        self.stdout.write("It is now %s" % time)
        print_date = datetime.date.today().strftime('%Y-%m-%d')
        self.stdout.write("The date is now %s" % print_date)
        string_print_date = str(print_date)
        date_time_scrape = print_date + ' ' + time
        self.stdout.write("The date and time is %s" % date_time_scrape)
        tz = timezone.get_current_timezone()
        print_date_time = datetime.datetime.now()
        print(print_date_time)
        print('Selenium Chrome opening ..')
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        print('Selenium Chrome is open')
        URL = 'https://www.python.org/'
        print('The current url will be printed on the next line')
        print(URL)
        # URL = 'https://helium-api.stakejoy.com/v1/hotspots/11N5DtCnKBGtcEGm7SieLcCCiQBZD8JBPddrAQdbSNwGExUapS3/rewards/sum?min_time=-14%20day&max_time=2023-01-31T00%3A00%3A00.000Z&bucket=day/'
        # when I switched to https it started working better.
        driver.get(URL)
        assert "Python" in driver.title
        print(driver.title)
        elem = driver.find_element(By.NAME, "q")
        elem.clear()
        elem.send_keys("pycon")
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source
        # elem = driver.find_element(By.NAME, 'p')
        another_url = "https://api.helium.io/v1/hotspots/11N5DtCnKBGtcEGm7SieLcCCiQBZD8JBPddrAQdbSNwGExUapS3/rewards/sum?min_time=-14%20day&max_time=2023-01-31T00%3A00%3A00.000Z&bucket=day"
        # print(elem)
        driver.close()
