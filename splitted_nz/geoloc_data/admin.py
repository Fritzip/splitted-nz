
from django.contrib.gis import admin
from .models import Spot
from leaflet.admin import LeafletGeoAdmin


class SpotAdmin(LeafletGeoAdmin):
    # fields to show in admin listview
    list_display = ('name', 'geometry')


# register models in the admin site
admin.site.register(Spot, SpotAdmin)