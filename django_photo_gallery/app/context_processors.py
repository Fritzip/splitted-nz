from django.shortcuts import render

from .models import Album

def albums(request):
    # album_list = list(set(map(lambda x : x['album'], list(Album.objects.values('album')))))
    # album_list.sort()
    # album_list = [(album,  Chord.objects.filter(album=album).count()) for album in album_list]

    album_list = Album.objects.filter(is_visible=True).order_by('-created')
    album_list = [(album.title, album.slug, album.created) for album in album_list]
    return {'album_list': album_list}
