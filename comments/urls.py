from django.urls.conf import path
from .views import getComments, add_Comment, delete_comment

urlpatterns = [
    path('getcomments/', getComments, name='Get_Comments'),
    path('add-comment/<int:blog_id>/<int:parent_id>/', add_Comment, name='Add-Comment'),
    path('delete-comment/<int:id>/<int:blog_id>/', delete_comment, name='Delete-Comment')
    
]