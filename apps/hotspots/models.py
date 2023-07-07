import string
import random
from autoslug import AutoSlugField
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from apps.common.models import TimeStampedUUIDModel

User = get_user_model()


class Hotspot(TimeStampedUUIDModel):
    hotspot_name = models.CharField(
        max_length=25,
        unique=True
    )
    hex_location = models.CharField(
        verbose_name=_('This is a shorter number next to a purple address sign.'),
        max_length=25
    )
    location_url = models.CharField(
        # This is a long string of numbers and characters next to an @ symbol.
        verbose_name=_('This string should be used as a variable in the URL.'),
        max_length=70,
        unique=True
    )
    slug = AutoSlugField(
        populate_from='hotspot_name',
        unique=True,
        # default='fakeslug',
        always_update=True
    )
    hotspot_manager = models.ForeignKey(
        User,
        verbose_name=_('Hotspot Manager'),
        related_name='hotspot_owner',
        on_delete=models.CASCADE,
    )
    homeowner_names = models.CharField(
        verbose_name=_('Homeowner names. Thirty characters or less.'),
        max_length=30,
        null=True,
        blank=True
    )
    street_address = models.CharField(
        verbose_name=_('Street Address'),
        max_length=150,
        default='123 Main Street',
        null=True,
        blank=True
    )
    city = models.CharField(
        verbose_name=_('City or Town'),
        max_length=100,
        default='Providence',
        null=True,
        blank=True
    )
    state_or_province = models.CharField(
        verbose_name=_('State or Province'),
        max_length=150,
        default='RI',
        null=True,
        blank=True
    )
    postal_code = models.CharField(
        verbose_name=_('Zipcode or Postal Code'),
        max_length=15,
        default='02901',
        null=True,
        blank=True
    )
    country = CountryField(
        verbose_name=_('Country'),
        default='US',
        blank_label='(select a country)',
        null=True,
        blank=True
    )
    phone_number = PhoneNumberField(
        verbose_name=_('Phone Number'),
        max_length=30,
        default='+12125552368',
        null=True,
        blank=True
    )
    general_notes = models.TextField(
        verbose_name=_('Notes, can be blank.'),
        null=True,
        blank=True
    )
    full_url = models.CharField(null=True)

    @property
    def full_url(self):
        return 'https://explorer.helium.com/hotspots/' + self.location_url + '/'

    def __str__(self):
        return f"{self.hotspot_name},{self.location_url}"
        # return '%s %s' % (self.hotspot_name, self.full_url)

    def get_absolute_url(self):
        return reverse('hotspot_detail', args=[str(self.pk)])  # chenged to .pk
        # instead of .id because this is what a user is sent to after creating
        # a new reward listing.

    class Meta:
        ordering = ['hotspot_name']
        unique_together = ['hotspot_name', 'location_url', 'hotspot_manager']
