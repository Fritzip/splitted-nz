#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import uuid
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.urls import reverse

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from datetime import datetime

def event_date(start, end):
    if end is None or start == end:
        return start.strftime("%d %b %Y")
    elif start.strftime("%b") == end.strftime("%b"):
        return start.strftime("%d") + " - " + end.strftime("%d %b %Y") 
    else:
        return start.strftime("%d %b") + " - " + end.strftime("%d %b %Y")

class Article(models.Model):
    title = models.CharField(max_length=70)
    description = models.TextField(max_length=8192)
    thumb = models.ImageField(upload_to='albums')
    is_visible = models.BooleanField(default=True)
    start_date = models.DateField(default=datetime.today)
    end_date = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=50, unique=True)

    #def get_absolute_url(self):
    #    return reverse('album', kwargs={'slug':self.slug})

    def get_event_date(self):
        return event_date(self.start_date, self.end_date)

    def __str__(self):
        return self.title

class ArticleImage(models.Model):
    # image = ProcessedImageField(upload_to='albums', processors=[ResizeToFit(1280)], format='JPEG', options={'quality': 70})
    image = models.ImageField(upload_to='albums')
    thumb = ImageSpecField(source='image',
                                      processors=[ResizeToFit(300)],
                                      format='JPEG',
                                      options={'quality': 10})

    album = models.ForeignKey(Article, on_delete=models.CASCADE)
    alt = models.CharField(max_length=255, default=uuid.uuid4)
    caption = models.TextField(max_length=2048, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    slug = models.SlugField(max_length=70, default=uuid.uuid4, editable=False)

@receiver(post_delete, sender=ArticleImage)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False) 

class Post(models.Model):
    text = models.TextField(max_length=1024)


from djgeojson.fields import PointField

class SleepSpot(models.Model):
    album = models.ForeignKey(Article, on_delete=models.PROTECT, blank=True, null=True)
    title = models.CharField(max_length=256)
    
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    geom = PointField(null=True, blank=True, default={})

    @property
    def popupContent(self):
        popup = '<b>{}</b><br>{}'.format(self.title, event_date(self.start_date, self.end_date))
        if self.album:
            article_link = 'Article : <a href="{}">{}</a>'.format(reverse('photo_gallery:article', args=(self.album.slug,)), self.album.title)
        else:
            article_link = 'Pas d\'article en rapport'
        
        popup += '<br><span class=article-link-popup>{}</span>'.format(article_link)

        popup += '<span class="btn-floating btn-small waves-effect waves-light zoom-in-popup"><i class="fas fa-compress-arrows-alt"></i></span>'

        return popup

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.album and not self.start_date:
            self.start_date = self.album.start_date
            self.end_date = self.album.end_date
        super(SleepSpot, self).save(*args, **kwargs)


    