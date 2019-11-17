from .models import DatedSpot
from django.contrib.gis import admin

from leaflet.admin import LeafletGeoAdmin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

class DatedSpotResource(resources.ModelResource):
    class Meta:
        model = DatedSpot

class DatedSpotAdmin(LeafletGeoAdmin, ImportExportModelAdmin):
    list_display = ('name', 'start_date', 'duration', 'album')
    resource_class = DatedSpotResource

# register models in the admin site
admin.site.register(DatedSpot, DatedSpotAdmin)