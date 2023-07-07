# Generated by Django 4.2.2 on 2023-06-27 13:31

import autoslug.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hotspot',
            fields=[
                ('pkid', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hotspot_name', models.CharField(max_length=25, unique=True)),
                ('hex_location', models.CharField(max_length=25, verbose_name='This is a shorter number next to a purple address sign.')),
                ('location_url', models.CharField(max_length=70, unique=True, verbose_name='This string should be used as a variable in the URL.')),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=False, populate_from='hotspot_name', unique=True)),
                ('homeowner_names', models.CharField(blank=True, max_length=30, null=True, verbose_name='Homeowner names. Thirty characters or less.')),
                ('street_address', models.CharField(blank=True, default='123 Main Street', max_length=150, null=True, verbose_name='Street Address')),
                ('city', models.CharField(blank=True, default='Providence', max_length=100, null=True, verbose_name='City or Town')),
                ('state_or_province', models.CharField(blank=True, default='RI', max_length=150, null=True, verbose_name='State or Province')),
                ('postal_code', models.CharField(blank=True, default='02901', max_length=15, null=True, verbose_name='Zipcode or Postal Code')),
                ('country', django_countries.fields.CountryField(blank=True, default='US', max_length=2, null=True, verbose_name='Country')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, default='+12125552368', max_length=30, null=True, region=None, verbose_name='Phone Number')),
                ('general_notes', models.TextField(blank=True, null=True, verbose_name='Notes, can be blank.')),
                ('hotspot_manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hotspot_owner', to=settings.AUTH_USER_MODEL, verbose_name='Hotspot Manager')),
            ],
            options={
                'ordering': ['hotspot_name'],
                'unique_together': {('hotspot_name', 'location_url', 'hotspot_manager')},
            },
        ),
    ]
