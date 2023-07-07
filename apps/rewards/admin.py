from django.contrib import admin

from .models import Reward


class RewardAdmin(admin.ModelAdmin):
    list_display = ['hotspot', 'timestamp', 'sum']
    list_filter = ['hotspot', 'timestamp', 'sum']


admin.site.register(Reward, RewardAdmin)
