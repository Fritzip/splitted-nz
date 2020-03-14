#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, shutil
import re
import uuid
import zipfile
import splitted_nz.settings
from datetime import datetime
from zipfile import ZipFile

from django.contrib import admin
from django.core.files.base import ContentFile
from django.urls import reverse

from PIL import Image

from .models import Article, ArticleImage
from .forms import ArticleForm

from import_export import resources
from import_export.admin import ImportExportModelAdmin

patt_xmpcaption = re.compile("<dc:description>(.*)<\/dc:description>")

class ArticleResource(resources.ModelResource):
    class Meta:
        model = Article

class ArticleAdmin(ImportExportModelAdmin):

    def pictures(self, obj):
        pics = ArticleImage.objects.filter(album=obj.id)
        out = ""
        for pic in pics:
            out += '<a href="{}"><img src="{}" width=350/></a>'.format(
                reverse("admin:photo_gallery_articleimage_change", args=[pic.id]),
                pic.image.url)

        return format_html(out)

    pictures.short_description = 'Pictures'

    readonly_fields = ('pictures',)

    form = ArticleForm
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'start_date','is_visible',)
    ordering = ('-start_date',)
    list_filter = ('start_date',)
    resource_class = ArticleResource

    def save_model(self, request, obj, form, change):
        uploadto = 'albums'
        if not os.path.exists(os.path.join(splitted_nz.settings.MEDIA_ROOT, uploadto)):
            os.makedirs(os.path.join(splitted_nz.settings.MEDIA_ROOT, uploadto))
        if form.is_valid():
            album = form.save(commit=False)
            album.modified = datetime.now()
            album.save()

            new_thumb_name = os.path.join(uploadto, 'thumb-{}.jpg'.format(album.slug))
            filepath_src = '{}{}'.format(splitted_nz.settings.MEDIA_ROOT, str(album.thumb))
            filepath_dest = '{}{}'.format(splitted_nz.settings.MEDIA_ROOT, new_thumb_name)

            album.thumb = new_thumb_name
            shutil.move(filepath_src, filepath_dest)
            album.save()

            if form.cleaned_data['zip'] != None:
                fzip = zipfile.ZipFile(form.cleaned_data['zip'])
                for filename in sorted(fzip.namelist()):

                    file_name = os.path.basename(filename)
                    if not file_name:
                        continue

                    data = fzip.read(filename)
                    contentfile = ContentFile(data)

                    img = ArticleImage()
                    img.album = album
                    img.alt = filename
                    xmp_start = data.find(b'<x:xmpmeta')
                    xmp_end = data.find(b'</x:xmpmeta')
                    xmp_str = re.findall(patt_xmpcaption, data[xmp_start:xmp_end+12].decode("utf-8"))
                    if xmp_str:
                        img.caption = xmp_str[0]
                    else:
                        img.caption = ""
                    filename = '{0}.jpg'.format(str(uuid.uuid4())[-12:])
                    directory = os.path.join(splitted_nz.settings.MEDIA_ROOT, uploadto, album.slug)
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    img.image.save(os.path.join(uploadto, album.slug, filename), contentfile)
                    filepath = os.path.join(directory, filename)
                    with Image.open(filepath) as i:
                        img.width, img.height = i.size

                    # img.thumb.save('thumb-{0}'.format(filename), contentfile)
                    img.save()
                fzip.close() 
            super(ArticleAdmin, self).save_model(request, obj, form, change)

admin.site.register(Article, ArticleAdmin)


class ArticleImageResource(resources.ModelResource):
    class Meta:
        model = ArticleImage

from django.utils.html import format_html

class ArticleImageAdmin(ImportExportModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" width=350/>'.format(obj.image.url))

    image_tag.short_description = 'Image'

    readonly_fields = ('image_tag',)
    list_display = ('id', 'alt', 'album')
    list_filter = ('album', 'created')
    resource_class = ArticleImageResource

admin.site.register(ArticleImage, ArticleImageAdmin)
