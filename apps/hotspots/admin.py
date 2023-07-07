from django.contrib import admin

from .models import Hotspot


class HotspotAdmin(admin.ModelAdmin):
    list_display = ['hotspot_name', 'hex_location',
                    'location_url', 'homeowner_names', 'hotspot_manager']


admin.site.register(Hotspot, HotspotAdmin)
