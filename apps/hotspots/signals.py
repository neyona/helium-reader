import logging
from django.db.models.signals import post_save
from django.dispatch import receiver

from hr_project.settings.base import AUTH_USER_MODEL
from .models import Hotspot

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Hotspot)
def create_hotspot(sender, instance, created, **kwargs):
    if created:
        Hotspot.objects.create(user=instance)
        instance.seed_database()


@receiver(post_save, sender=Hotspot)
def save_hotspot(sender, instance, **kwargs):
    instance.hotspot.save()
    logger.info(f"The {instance} hotspot has been created")
