from django_countries.serializer_fields import CountryField
from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers

from .models import Hotspot
from apps.rewards.models import Reward
from apps.rewards.serializers import RewardSerializer


class HotspotSerializer(CountryFieldMixin, serializers.ModelSerializer):
    reward = RewardSerializer(many=True)
    country = CountryField(name_only=True)

    class Meta:
        model = Hotspot
        fields = [
            'pkid',
            'id',
            'hotspot_name',
            'hex_location',
            'location_url',
            'slug',
            'hotspot_manager',
            'homeowner_names',
            'street_address',
            'city',
            'postal_code',
            'state_or_province',
            'country',
            'phone_number',
            'general_notes',
            'full_url',
            'reward',
        ]

    def create(self, validated_data):
        reward_data = validated_data.pop('reward')
        hotspot = Hotspot.objects.create(**validated_data)
        for reward_data in reward_data:
            Reward.objects.create(reward=reward, **reward_data)
        return hotspot


class HotspotCreateSerializer(CountryFieldMixin, serializers.ModelSerializer):
    country = CountryField(name_only=True)

    class Meta:
        model = Hotspot
        exclude = ['updated_at', ]  # this means TimeStampedUUIDModel is excluded
