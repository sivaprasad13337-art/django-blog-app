from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils.text import slugify
import os, datetime

def upload_file(instance, filename):
    time = datetime.datetime.now().strftime('%d-%m-%y_%H-%M-%S')
    name, ext = os.path.splitext(filename)
    new_filename = f"{name}_{time}{ext}"
    return os.path.join('uploads', new_filename)

class BlogCategories(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    image = models.ImageField(upload_to=upload_file, blank=False, null=False)
    quote = models.CharField(max_length=300, blank=False, null=False)
    short_qoute = models.CharField(max_length=200, blank=False, null=False)
    C_code = models.CharField(max_length=12, blank=False, null=False)
    likes = models.IntegerField(null=False, blank=False)
    views = models.IntegerField(null=False, blank=False)
    saves = models.IntegerField(null=False, blank=False)
    
    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    slug = models.SlugField(unique=True, blank=True)
    content = RichTextField()
    image = models.ImageField(upload_to=upload_file, blank=False, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(BlogCategories, on_delete=models.PROTECT, related_name='posts')
    post_tag = models.CharField(max_length=300, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=1,null=False, blank=False)
    views = models.IntegerField(default=30,null=False, blank=False)
    saves = models.IntegerField(default=0,null=False, blank=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            count = 1

            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title