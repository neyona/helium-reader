from rest_framework import serializers

from .models import Reward
from apps.hotspots.models import Hotspot


class RewardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reward
        fields = [
            'hotspot',
            'date_celery_added_instance_to_database',
            'timestamp',
            'sum',
            'comment_in_case_of_change'
        ]
