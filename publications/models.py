from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from profiles.models import User


def upload_location(instance, filename, **kwargs):
    file_path = 'post/{author_id}/{title}-{filename}'.format(
        author_id=str(instance.author.id), title=str(instance.title), filename=filename
    )
    return file_path


class Post(models.Model):
    title = models.CharField(max_length=50, null=True, blank=False)
    body = models.TextField(max_length=5000, null=False, blank=False)
    image = models.ImageField(upload_to=upload_location, null=True, blank=False)
    date_published = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='likes')
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.title


@receiver(post_delete, sender=Post)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)


def pre_save_post_receiever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username + "-" + instance.title)


pre_save.connect(pre_save_post_receiever, sender=Post)
