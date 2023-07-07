from celery import shared_task, current_app
import os
import json
import datetime
import pandas as pd
import numpy as np
from django.utils import timezone, dateparse
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from urllib.request import urlopen

from celery.utils.log import get_task_logger
from django.core.management import call_command

# from celery.task.schedules import crontab
# from celery.decorators import periodic_task

from .serializers import HotspotSerializer
from apps.rewards.serializers import RewardSerializer
from .models import Hotspot
from apps.rewards.models import Reward

logger = get_task_logger(__name__)


@shared_task
def adding_task(x, y, items=[]):
    result = x + y
    if items:
        for x, y in items:
            result += (x + y)
    return result


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def sample_task():
    logger.info("The sample task just ran.")


@shared_task
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True


@shared_task
def seed_task():
    logger.info("The first 60 entries have been added.")


@shared_task(name="Populate the first 60 reward instances")
def seed_database(hotspot_id):
    hotspot = HotspotModel.objects.get(id=hotspot_id)
    call_command("helium_sixty", )
    print("Finished setting up the first sixty instances for {hotspot_name}.".format(
        hotspot_name=hotspot.hotspot_name))
