from django.contrib import admin
from .models import BlogCategories, Post

# Register your models here.
admin.site.register(BlogCategories)
admin.site.register(Post)