from django.urls import path
from .views import like_post, save_post, follow_user

urlpatterns = [
    path('like-post/<int:blog>/', like_post, name='Like-Post'),
    # path('unlike-post/<int:blog>/', unlike_post, name='Unlike-Post'),
    path('save-post/<int:blog>/', save_post, name='Save-Post'),
    # path('unsave-post/<int:blog>/', unsave_post, name='Unsave-Post'),
    path('follow-user/<int:user_id>/', follow_user, name='Follow-User')
]