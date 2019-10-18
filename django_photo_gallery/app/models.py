#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import uuid
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
 
# from imagekit.models import ProcessedImageField
# from imagekit.processors import ResizeToFit
from datetime import datetime

class Album(models.Model):
    title = models.CharField(max_length=70)
    description = models.TextField(max_length=8192)
    # thumb = ProcessedImageField(upload_to='albums', processors=[ResizeToFit(1280)], format='JPEG', options={'quality': 70})
    thumb = models.ImageField(upload_to='albums')
    tags = models.CharField(max_length=250)
    is_visible = models.BooleanField(default=True)
    start_date = models.DateField(default=datetime.today)
    end_date = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=50, unique=True)

    #def get_absolute_url(self):
    #    return reverse('album', kwargs={'slug':self.slug})

    def get_event_date(self):
        if self.end_date is None or self.start_date == self.end_date:
            return self.start_date.strftime("%d %b %Y")
        else:
            return self.start_date.strftime("%d %b") + " - " + self.end_date.strftime("%d %b %Y")

    def __unicode__(self):
        return self.title

class AlbumImage(models.Model):
    # image = ProcessedImageField(upload_to='albums', processors=[ResizeToFit(1280)], format='JPEG', options={'quality': 70})
    image = models.ImageField(upload_to='albums')
    # thumb = ProcessedImageField(upload_to='albums', processors=[ResizeToFit(500)], format='JPEG')#, options={'quality': 90})
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    alt = models.CharField(max_length=255, default=uuid.uuid4)
    caption = models.CharField(max_length=2048, default='')
    created = models.DateTimeField(auto_now_add=True)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    slug = models.SlugField(max_length=70, default=uuid.uuid4, editable=False)

@receiver(post_delete, sender=AlbumImage)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False) 

class Post(models.Model):
    text = models.TextField(max_length=1024)