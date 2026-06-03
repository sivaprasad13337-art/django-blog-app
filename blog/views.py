from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import PostForm
from .models import Post, BlogCategories
from comments.form import CommentsForm
from comments.models import CommentsModel
from accounts.models import Profile
from utils.models import LikesModel, SaveModel
from .utils import verify_views

# Create your views here.
def default(request):
    return render(request, 'blog/layouts/base.html')

@login_required(login_url='/users/login/')
def getHome(request):
    posts = Post.objects.all().order_by('-created_at')
    categories = BlogCategories.objects.all()
    viewed_posts = request.session.get('viewed_posts', [])
    
    liked_posts = LikesModel.objects.filter(user = request.user)
    saved_posts = SaveModel.objects.filter(user = request.user)
    
    liked = list(map(lambda x:x.post, liked_posts))
    saved = list(map(lambda x:x.post, saved_posts))
    
    # if post == liked_posts[1]:
    #     print(True)
    # else:
    #     print(False)
    return render(request, 'blog/home.html', {
        'posts': posts,
        'categories': categories,
        'viewed_posts': viewed_posts,
        'liked': liked,
        'saved': saved
    })

@login_required(login_url='/users/login/')
def post_blog(request):
    categories = BlogCategories.objects.all()
    profile = get_object_or_404(Profile, user = request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            profile.posts += 1
            profile.save()
            return redirect('Get-Home')
    else:
        form = PostForm()
    return render(request, 'blog/post_blog.html', {'categories': categories,'form': form})


@login_required(login_url='/users/login/')
def get_blog_by_slug(request, slug):
    blog = get_object_or_404(Post, slug=slug)
    related_posts = Post.objects.filter(category=blog.category).exclude(id=blog.id)[:3]
    comment_form = CommentsForm()
    comments = CommentsModel.objects.filter(blog=blog)
    
    verify_views(request, blog)
    
    liked_post = LikesModel.objects.filter(user = request.user, post = blog).first()
    saved_post = SaveModel.objects.filter(user = request.user, post = blog).first()
    
    return render(request, 'blog/blog_page.html', {'blog': blog, 'related_posts': related_posts,'comment_form': comment_form, 'comments': comments, 'liked_post': liked_post, 'saved_post': saved_post})

@login_required(login_url='/users/login/')
def get_categories(request):
    categories = BlogCategories.objects.all()
    return render(request, 'blog/categories.html', {'categories': categories})

@login_required(login_url='/users/login/')
def get_blog_by_category(request, cat_id):
    category = get_object_or_404(BlogCategories, id=cat_id)
    posts = category.posts.all().order_by('-created_at')
    
    return render(request, 'blog/category_page.html', {'category': category,'posts': posts})


# @login_required(login_url='/users/login/')
# def get_posts_by_author(request, author_id):
#     posts = Post.objects.filter(author_id = author_id)
#     return render(request, 'accounts/profile.html', {'posts': posts})


@login_required(login_url='/users/login/')
def set_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.user != post.author:
        return render(request, 'blog/edit_blog.html', { 'error': "403 Forbidden: You don't have permission to edit this post"})
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('GET-BLOG', slug = post.slug)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/edit_blog.html', {'form': form})

@login_required(login_url='/users/login/')
def delete_post(request, slug):
    blog = get_object_or_404(Post, slug = slug)
    print(blog)
    
    if request.user == blog.author:
        blog.delete()
        return redirect('Get-Profile', user_name = request.user.username)
    else:
        return render(request, 'error.html', {'error':"You don't permisson to delete this blog"})
    
    
        
@login_required(login_url='/users/login/')
def search(request):
   
   if request.method == 'POST':
        option = request.POST['option']
        query = request.POST['query']
       
        if option == 'User':
            users = User.objects.filter(Q(username__icontains = query) | Q(first_name__icontains = query) | Q(last_name__icontains = query))
            
            
            return render(request, 'blog/search_results.html', {
                'users': users,
                # 'length': length
                })
            
        elif option == 'Category':
            categories = BlogCategories.objects.filter(Q(name__icontains = query))
            
            return render(request, 'blog/search_results.html', {'categories': categories})
   
        else:
            posts = Post.objects.filter(Q(title__icontains = query) | Q(content__icontains = query) | Q(post_tag__icontains = query))
            # categories = BlogCategories.objects.all()
            viewed_posts = request.session.get('viewed_posts', [])
        
            liked_posts = LikesModel.objects.filter(user = request.user)
            saved_posts = SaveModel.objects.filter(user = request.user)
        
            liked = list(map(lambda x:x.post, liked_posts))
            saved = list(map(lambda x:x.post, saved_posts))
        
            if posts:
                return render(request, 'blog/search_results.html', {
                'posts': posts,
                # 'categories': categories,
                'viewed_posts': viewed_posts,
                'liked': liked,
                'saved': saved
                })
          
   else:
        return render(request, 'blog/search_results.html')
        