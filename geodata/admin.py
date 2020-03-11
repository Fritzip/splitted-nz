from .models import StravActivity, SleepSpot
from photo_gallery.models import Article

from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.contrib import admin

from leaflet.admin import LeafletGeoAdmin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from django.conf.locale.en import formats as en_formats
en_formats.DATETIME_FORMAT = "d M Y - H:i"
                       

def set_article(modeladmin, request, queryset):
    if 'apply' in request.POST:
        if request.POST['selected_article'] == "reset":
            queryset.update(article=None)
            modeladmin.message_user(request, "Reset related article for {} entries".format(queryset.count()))
        elif request.POST['selected_article'] != "" :
            selected_article = Article.objects.get(id=request.POST['selected_article'])
            queryset.update(article=selected_article)
            modeladmin.message_user(request, "Changed related article to {} for {} entries".format(selected_article, queryset.count()))
        else:
            modeladmin.message_user(request,
                              "Unchanged related article")
        return HttpResponseRedirect(request.get_full_path())

    return render(request,
                  'admin/set_article_intermediate.html',
                  context={'articles': Article.objects.order_by('-start_date'), 'orders':queryset})

set_article.short_description = "Set the related article for selected items"

class SleepSpotResource(resources.ModelResource):
    class Meta:
        model = SleepSpot

class SleepSpotAdmin(LeafletGeoAdmin, ImportExportModelAdmin):
    list_display = ('name', 'start_date', 'duration', 'article')
    ordering = ('-start_date',)
    actions = [set_article]
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
    actions = [set_article]
    resource_class = StravActivityResource

admin.site.register(StravActivity, StravActivityAdmin)
