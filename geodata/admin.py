from .models import StravActivity, SleepSpot

from django.contrib import admin

from leaflet.admin import LeafletGeoAdmin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from django.conf.locale.en import formats as en_formats
en_formats.DATETIME_FORMAT = "d M Y - H:i"

class SleepSpotResource(resources.ModelResource):
    class Meta:
        model = SleepSpot

class SleepSpotAdmin(LeafletGeoAdmin, ImportExportModelAdmin):
    list_display = ('name', 'start_date', 'duration', 'article')
    ordering = ('-start_date',)
    resource_class = SleepSpotResource
    settings_overrides =  {
        'DEFAULT_CENTER': (-43.2016, 171.243), #for lack of anything better
        'DEFAULT_ZOOM': 8,
    }

admin.site.register(SleepSpot, SleepSpotAdmin)

class StravActivityResource(resources.ModelResource):
    class Meta:
        model = StravActivity

class StravActivityAdmin(LeafletGeoAdmin, ImportExportModelAdmin):
    list_display = ('name', 'status', 'start_date_local', 'distance', 'article')
    list_filter = ('start_date_local', 'status')
    ordering = ('-start_date_local',)
    resource_class = StravActivityResource

admin.site.register(StravActivity, StravActivityAdmin)
