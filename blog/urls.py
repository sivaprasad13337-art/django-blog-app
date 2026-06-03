from django.urls.conf import path
from .views import getHome, post_blog, get_blog_by_slug, default, get_categories, get_blog_by_category, set_post, delete_post, search

urlpatterns = [
    path('', default, name='root'),
    path('home/', getHome, name='Get-Home'),
    path('post-blog/', post_blog, name='POST-BLOG'),
    path('set-post/<int:post_id>', set_post, name='Set-Post'),
    path('get-blog/<str:slug>/', get_blog_by_slug, name='GET-BLOG'),
    path('delete-post/<str:slug>', delete_post, name='Delete-Blog'),
    # path('posts/<int:author_id>/', get_posts_by_author, name='Get-Posts-by-Author'),
    path('get-categories/', get_categories, name='Get-Categories'),
    path('get-category/<int:cat_id>', get_blog_by_category, name='Get-Category'),
    path('search/', search, name='Search')
]