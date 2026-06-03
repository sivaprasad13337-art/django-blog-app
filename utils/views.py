from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from blog.models import Post, BlogCategories
from accounts.models import Profile, User
from .models import LikesModel, SaveModel, FollowModel
from django.db import transaction
from django.db.models import F, Value
from django.db.models.functions import Greatest


@login_required(login_url='/users/login/')
def like_post(request, blog):
    # if request.method != "POST":
    #     return redirect('GET-BLOG', slug=blog)

    user = request.user
    blog = get_object_or_404(Post, id=blog)

    like = LikesModel.objects.filter(user=user, post=blog).first()

    with transaction.atomic():
        if like:
            like.delete()

            Post.objects.filter(id=blog.id).update(
                likes=Greatest(F('likes') - 1, Value(0))
            )

            BlogCategories.objects.filter(id=blog.category.id).update(
                likes=Greatest(F('likes') - 1, Value(0))
            )

        else:
            LikesModel.objects.create(user=user, post=blog)

            Post.objects.filter(id=blog.id).update(
                likes=F('likes') + 1
            )

            BlogCategories.objects.filter(id=blog.category.id).update(
                likes=F('likes') + 1
            )
    print(f'this is {blog.slug}')
    return redirect('GET-BLOG', slug = blog.slug)
    
# @login_required()
# def unlike_post(request):
#     user = request.user
#     blog = get_object_or_404(Post, id = blog)
#     like = get_object_or_404(LikesModel,user = user, post = blog)
#     print(like)
    
#     if like:
#         like.delete()
#         return redirect('GET-BLOG', slug = blog.slug)
#     else:
#         return render(request,'utils/error.html', {'error': 'facing error while removing like to this post'})


@login_required(login_url='/users/login/')
def save_post(request, blog):
    # if request.method != "POST":
    #     return redirect('GET-BLOG', slug=blog)

    user = request.user
    blog = get_object_or_404(Post, id=blog)

    save_model = SaveModel.objects.filter(user=user, post=blog).first()

    with transaction.atomic():
        if save_model:
            save_model.delete()

            Post.objects.filter(id=blog.id).update(
                saves=Greatest(F('likes') - 1, Value(0))
            )

            BlogCategories.objects.filter(id=blog.category.id).update(
                saves=Greatest(F('likes') - 1, Value(0))
            )

        else:
            SaveModel.objects.create(user=user, post=blog)

            Post.objects.filter(id=blog.id).update(
                saves=F('likes') + 1
            )

            BlogCategories.objects.filter(id=blog.category.id).update(
                saves=F('likes') + 1
            )
            
    return redirect('GET-BLOG', slug = blog.slug)
    

# @login_required()
# def unsave_post(request):
#     user = request.user
#     blog = get_object_or_404(Post, id = blog)
#     save_model = SaveModel.objects.filter(user = user, post = blog)
#     print(save_model)
    
#     if save_model:
#         save_model.delete()
#         return redirect('GET-BLOG', slug = blog.slug)
#     else:
#         return render(request,'utils/error.html', {'error': 'facing error while removing this post from you savelist'})

@login_required(login_url='/users/login/')
def follow_user(request, user_id):
    user = get_object_or_404(User, id = user_id)
    follower = request.user
    
    follow_model = FollowModel.objects.filter(user = user, follower = follower)
    
    with transaction.atomic():
       if follow_model:
           follow_model.delete()
           Profile.objects.filter(user = user).update(followers = Greatest(F('followers') - 1, Value(0)))
           
           Profile.objects.filter(user = follower).update(following = Greatest(F('following') - 1, Value(0)))
        
       else:
           FollowModel.objects.create(user = user, follower = follower)
           
           Profile.objects.filter(user = user).update(
                followers=F('followers') + 1
            )
           
           Profile.objects.filter(user = follower).update(
                following=F('following') + 1
            )
        
    return redirect('Get-Profile', user.username)
        
    
