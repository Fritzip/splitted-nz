from django.shortcuts import render

from photo_gallery.models import Article

def articles(request):
    article_list = Article.objects.filter(is_visible=True).order_by('-start_date')    
    article_list = [(article.title, article.slug, article.get_event_date, article.thumb) for article in article_list]
    return {'article_list_cp': article_list}
