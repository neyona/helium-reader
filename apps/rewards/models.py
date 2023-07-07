
import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from apps.hotspots.models import Hotspot
from apps.common.models import TimeStampedUUIDModel
"""
it is set up as such so it subclasses the TimeStampedUUIDModel it might not
be needed.

I made it so the user who inputted hotspot is able to fix the data here in
these model instances in case something goes wrong. I added an optional
comment box to keep track of that kind of change.

"""
User = get_user_model()


class Reward(TimeStampedUUIDModel):
    hotspot = models.ForeignKey(
        Hotspot,
        verbose_name=_('The name the of hotspot'),
        related_name='reward',  # might clash against HotspotModel without this
        to_field='hotspot_name',
        on_delete=models.CASCADE,  # cascade means that when the hotspot is
        # deleted, the instances with it will be as well.
    )
    date_celery_added_instance_to_database = models.DateTimeField()
    # this should be the date on the day under timestamp
    timestamp = models.DateField()
    # this corresponds with dictionary heading called sum
    sum = models.IntegerField(null=True)
    comment_in_case_of_change = models.TextField(
        verbose_name=_('Description of Correction'),
        default='A comment should be left if a reward is changed saying why it was made.',
        blank=True
    )

    def get_absolute_url(self):
        return reverse('reward_detail', args=[str(self.pk)])  # changed to .pk
        # instead of .id because this is what a user is sent to after creating
        # a new hotspot.

    class Meta:
        ordering = ['timestamp']
        unique_together = ['hotspot', 'timestamp']

    def __str__(self):
        return f'{self.hotspot} checked on {self.date_celery_added_instance_to_database}'
        # this should help with getting information one week at a time.
