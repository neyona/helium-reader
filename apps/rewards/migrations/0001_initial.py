# Generated by Django 4.2.2 on 2023-06-27 13:31

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hotspots', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('pkid', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date_celery_added_instance_to_database', models.DateTimeField()),
                ('timestamp', models.DateField()),
                ('sum', models.IntegerField(null=True)),
                ('comment_in_case_of_change', models.TextField(blank=True, default='A comment should be left if a reward is changed saying why it was made.', verbose_name='Description of Correction')),
                ('hotspot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reward', to='hotspots.hotspot', to_field='hotspot_name', verbose_name='The name the of hotspot')),
            ],
            options={
                'ordering': ['timestamp'],
                'unique_together': {('hotspot', 'timestamp')},
            },
        ),
    ]
