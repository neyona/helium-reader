from django.urls import path, include

from .views import (
    HotspotDetailView,
    RewardDetailView,
    HotspotListView,
    RewardListView,
    HotspotUpdateView,
    RewardUpdateView,
    HotspotDeleteView,
    HotspotCreateView,
    RewardDeleteView,
    RewardCreateView,
    HotspotListSerializer,
    RewardListSerializer,
    HotspotDetailSerializer,
    RewardDetailSerializer
)

urlpatterns = [
    path('api/<int:pk>/', HotspotDetailSerializer.as_view()),
    path('api/rewards/<int:pk>/', RewardDetailSerializer.as_view()),
    path('api/', HotspotListSerializer.as_view()),
    path('api/rewards/', RewardListSerializer.as_view()),
    path('<int:pk>/edit/', HotspotUpdateView.as_view(), name='hotspot_edit'),
    path('reward/<int:pk>/edit/',
         RewardUpdateView.as_view(), name='reward_edit'),
    path('<int:pk>/delete/', HotspotDeleteView.as_view(), name='hotspot_delete'),
    path('reward/<int:pk>/delete/',
         RewardDeleteView.as_view(), name='reward_delete'),
    path('<int:pk>/', HotspotDetailView.as_view(), name='hotspot_detail'),
    path('rewards/<int:pk>/',
         RewardDetailView.as_view(), name='reward_detail'),
    path('new/', HotspotCreateView.as_view(), name='hotspot_new'),
    path('reward/new/', RewardCreateView.as_view(), name='reward_new'),
    path('reward/', RewardListView.as_view(), name='reward_list'),
    path('', HotspotListView.as_view(), name='hotspot_list'),
]
