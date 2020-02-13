from .models import StravActivity

from django.contrib import admin

from leaflet.admin import LeafletGeoAdmin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

class StravActivityResource(resources.ModelResource):
    class Meta:
        model = StravActivity

class StravActivityAdmin(LeafletGeoAdmin, ImportExportModelAdmin):
    list_display = ('name', 'status', 'start_date_local', 'distance', 'article')
    list_filter = ('start_date_local', 'status')
    ordering = ('-start_date_local',)
    resource_class = StravActivityResource

admin.site.register(StravActivity, StravActivityAdmin)
