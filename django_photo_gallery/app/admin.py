#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import uuid
import zipfile
import django_photo_gallery.settings
from datetime import datetime
from zipfile import ZipFile

from django.contrib import admin
from django.core.files.base import ContentFile

from PIL import Image

from app.models import Album, AlbumImage, SleepSpot
from app.forms import AlbumForm

patt_xmpcaption = re.compile("<dc:description>(.*)<\/dc:description>")

@admin.register(Album)
class AlbumModelAdmin(admin.ModelAdmin):
    form = AlbumForm
    prepopulated_fields = {'slug': ('title',)}
    # list_display = ('title', 'start_date')
    list_filter = ('start_date',)

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            album = form.save(commit=False)
            album.modified = datetime.now()
            album.save()
            if form.cleaned_data['zip'] != None:
                fzip = zipfile.ZipFile(form.cleaned_data['zip'])
                for filename in sorted(fzip.namelist()):

                    file_name = os.path.basename(filename)
                    if not file_name:
                        continue

                    data = fzip.read(filename)
                    contentfile = ContentFile(data)

                    img = AlbumImage()
                    img.album = album
                    img.alt = filename
                    xmp_start = data.find(b'<x:xmpmeta')
                    xmp_end = data.find(b'</x:xmpmeta')
                    xmp_str = re.findall(patt_xmpcaption, data[xmp_start:xmp_end+12].decode("utf-8"))
                    if xmp_str:
                        img.caption = xmp_str[0]
                    else:
                        img.caption = ""
                    filename = '{0}{1}.jpg'.format(album.slug, str(uuid.uuid4())[-13:])
                    img.image.save(filename, contentfile)
                
                    filepath = '{0}/albums/{1}'.format(django_photo_gallery.settings.MEDIA_ROOT, filename)
                    with Image.open(filepath) as i:
                        img.width, img.height = i.size

                    # img.thumb.save('thumb-{0}'.format(filename), contentfile)
                    img.save()
                fzip.close() 
            super(AlbumModelAdmin, self).save_model(request, obj, form, change)

@admin.register(AlbumImage)
class AlbumImageModelAdmin(admin.ModelAdmin):
    list_display = ('alt', 'album')
    list_filter = ('album', 'created')

from leaflet.admin import LeafletGeoAdmin
from import_export import resources
from import_export.fields import Field
from import_export.admin import ImportExportModelAdmin
import json

from djgeojson.fields import PointField

class SleepSpotResource(resources.ModelResource):
    latitude = Field(attribute='latitude', column_name='latitude')
    longitude = Field(attribute='longitude', column_name='longitude')

    class Meta:
        model = SleepSpot
        fields = ('id','album','title','start_date','end_date','latitude','longitude' )
        exclude = ('geom')
        export_order = ('id','album','title','start_date','end_date','latitude','longitude' )

    def before_save_instance(self, instance, using_transactions, dry_run):
        longitude = float(getattr(instance, 'longitude'))
        latitude = float(getattr(instance, 'latitude'))

        instance.geom = {'type': 'Point', 'coordinates': [longitude, latitude]}
        return instance

    def dehydrate_longitude(self, sleepspot):
        try:
            geomjson = sleepspot.geom
            if type(geomjson) is str:
                geomjson = json.loads(geomjson.replace("\'", "\""))
            return geomjson['coordinates'][0]
        except:
            pass

    def dehydrate_latitude(self, sleepspot):
        try:
            geomjson = sleepspot.geom
            if type(geomjson) is str:
                geomjson = json.loads(geomjson.replace("\'", "\""))
            return geomjson['coordinates'][1]
        except:
            pass

@admin.register(SleepSpot)
class SleepSpotModelAdmin(LeafletGeoAdmin, ImportExportModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'album')
    resource_class = SleepSpotResource
