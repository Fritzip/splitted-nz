import splitted_nz.settings
from photo_gallery.models import ArticleImage, Article

qs = ArticleImage.objects.all()
for ss in qs:
    new_img_path = str(ss.image)
    k = os.path.basename(new_img_path).rfind("-")
    if k >= 0:
        new_img_path = new_img_path[:k] + "/" + new_img_path[k+1:]
        filepath_src = '{}{}'.format(splitted_nz.settings.MEDIA_ROOT, str(ss.image))
        filepath_dest = '{}{}'.format(splitted_nz.settings.MEDIA_ROOT, new_img_path)
        if not os.path.exists(os.path.dirname(filepath_dest)):
            os.makedirs(os.path.dirname(filepath_dest))

        ss.image = new_img_path 
        os.rename(filepath_src, filepath_dest)
        ss.save()

qs = Article.objects.all()
for ss in qs:
    new_thumb_name = str(ss.thumb)
    dirname = os.path.dirname(new_thumb_name)
    new_thumb_name = os.path.join(dirname, 'thumb-{}.jpg'.format(ss.slug))
    filepath_src = '{}{}'.format(splitted_nz.settings.MEDIA_ROOT, str(ss.thumb))
    filepath_dest = '{}{}'.format(splitted_nz.settings.MEDIA_ROOT, new_thumb_name)

    ss.thumb = new_thumb_name
    os.rename(filepath_src, filepath_dest)
    ss.save()
    