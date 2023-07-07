import logging
import redis

# import django_filters
# from django_filters.rest_framework import DjangoFilterBackend

from django.db import transaction
from django.core.management import call_command
from django.db.models import query
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, UpdateView, DeleteView, CreateView

from rest_framework import filters, status
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from rest_framework_api_key.permissions import HasAPIKey

from celery import shared_task, current_app

from .models import Hotspot
from .serializers import HotspotSerializer, HotspotCreateSerializer
from apps.rewards.models import Reward
from apps.rewards.serializers import RewardSerializer
# from .tasks import seed_database, seed_task
from .exceptions import HotspotNotFound

logger = logging.getLogger(__name__)


class HotspotListView(LoginRequiredMixin, ListView):
    model = Hotspot
    context_object_name = 'hotspot_list'
    queryset = Hotspot.objects.all()
    template_name = 'hotspot_list.html'
    login_url = 'login'


class RewardListView(LoginRequiredMixin, ListView):
    model = Reward
    context_object_name = 'reward_list'
    queryset = Reward.objects.all()
    template_name = 'reward_list.html'
    login_url = 'login'


class HotspotDetailView(LoginRequiredMixin, DetailView):
    model = Hotspot
    context_object_name = 'hotspot'
    queryset = Hotspot.objects.all()
    template_name = 'hotspot_detail.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reward_list'] = Reward.objects.filter(hotspot=self.object.hotspot_name).all()
        # did not work with self.objects.id instead used self.object.hotspot_name
        return context

class RewardDetailView(LoginRequiredMixin, DetailView):
    model = Reward
    context_object_name = 'reward'
    queryset = Reward.objects.all()
    template_name = 'reward_detail.html'
    login_url = 'login'


class HotspotUpdateView(LoginRequiredMixin, UpdateView):
    model = Hotspot
    fields = '__all__'
    template_name = 'hotspot_edit.html'
    success_url = reverse_lazy('hotspot_list')
    login_url = 'login'


class RewardUpdateView(LoginRequiredMixin, UpdateView):
    model = Reward
    fields = '__all__'
    template_name = 'reward_edit.html'
    success_url = reverse_lazy('reward_list')
    login_url = 'login'


class HotspotDeleteView(LoginRequiredMixin, DeleteView):
    model = Hotspot
    template_name = 'hotspot_delete.html'
    success_url = reverse_lazy('hotspot_list')
    login_url = 'login'


class RewardDeleteView(LoginRequiredMixin, DeleteView):
    model = Reward
    template_name = 'reward_delete.html'
    success_url = reverse_lazy('reward_list')
    login_url = 'login'


class HotspotCreateView(LoginRequiredMixin, CreateView):
    model = Hotspot
    template_name = 'hotspot_new.html'
    fields = '__all__'
    login_url = 'login'

    def form_valid(self, form):
        form.instance.hotspot_manager = self.request.user
        response = super().form_valid(form)
        hotspot_id = self.object.id
        transaction.on_commit(
            lambda: current_app.send_task(
                call_command('helium_sixty', hotspot_id),
                kwargs={"hotspot_id": self.object.id}
            )
        )
        return response


class RewardCreateView(LoginRequiredMixin, CreateView):
    model = Reward
    template_name = 'reward_new.html'
    fields = '__all__'
    login_url = 'login'

    def form_valid(self, form):
        form.instance.hotspot = self.request.user
        return super().form_valid(form)


class HotspotListSerializer(ListCreateAPIView):
    queryset = Hotspot.objects.all()
    serializer_class = HotspotSerializer


class RewardListSerializer(ListCreateAPIView):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer


class HotspotDetailSerializer(RetrieveUpdateDestroyAPIView):
    queryset = Hotspot.objects.all()
    serializer_class = HotspotSerializer


class RewardDetailSerializer(RetrieveUpdateDestroyAPIView):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer
