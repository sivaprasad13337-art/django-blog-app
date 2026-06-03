from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Profile
from .forms import ProfileForm, UserForm
from blog.models import Post
from utils.models import FollowModel, LikesModel, SaveModel
from .utils import does_user_exists, fun
from django.http import HttpResponse

# Create your views here.
def old_url(request):
    return redirect('NEW-URL')

def new_url(request):
    return HttpResponse('This is New One ey!')

def index(request):
    fun(request)
    return render(request, 'accounts/layouts/main.html')

def createUser(request):
    
    if request.user.is_authenticated:
        return redirect('Get-Home')
    
    if request.method == 'POST':
        form = UserForm(request.POST)
        
        if does_user_exists(request.POST['username']):
            return render(request, 'accounts/register.html', {
                'form': form,
                'error': 'User Already Exists!'
            })

        if(form.is_valid()):
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('Login-User')
    else:
        form = UserForm()
    return render(request, 'accounts/register.html', {'form': form})


################################################---LOGIN---#################################################
# POST → authenticate → login → redirect
# GET  → show login page
def userLogin(request):
    
    if request.user.is_authenticated:
        return redirect('Get-Home')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password) #Auth Handles User exists n validating.

        if user is not None:
            login(request, user)
            return redirect('Get-Home')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid Credentials'})

    return render(request, 'accounts/login.html')
# Auth Flow
# login()
# ↓
# session created
# ↓
# sessionid stored in cookie
# ↓
# browser sends sessionid each request
# ↓
# Django finds session
# ↓
# loads user
# ↓
# sets request.user
################################################---LOGIN---#################################################

@login_required
def userLogout(request):
    logout(request)
    return redirect('Login-User')

################################################---SET-PROFILE---#################################################            
# @login_required
# ↓
# check session cookie
# ↓
# verify session
# ↓
# get user
# ↓
# attach to request.user
# ↓
# request.user.profile
# ↓
# return profile
@login_required(login_url='/users/login/')
def setProfile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    user = get_object_or_404(User, id = request.user.id)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance = profile)
        
        username = request.POST['username']
        first_name = request.POST['firstname']
        second_name = request.POST['secondname']
        
        # if request.POST['username'] is not request.user:
        #     if does_user_exists(request.POST.[username]):
        #         return render(request, 'accounts/editProfile.html', {'error': f"@{request.POST['username']} already taken!"})
            
        if form.is_valid():
            print('the form is valid')
            print(f"here's the file{request.FILES}")
            form.save()
            
            user.username = username
            user.first_name = first_name
            user.last_name = second_name
            user.save()
            print('success')
            return redirect('Get-Profile', user_name = profile.user.username)
    else:
        print("somthin's wrong")
        profile = ProfileForm(instance=profile)
        user_form = user
    return render(request, 'accounts/editProfile.html', {'profile': profile, 'user': user_form})

# @login_required
# def createProfile(request):
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES)
#         if(form.is_valid()):
#             profile = form.save(commit=False)
#             profile.user = request.user
#             profile.save()
            
#             return redirect('/getProfile')
#     else:
#         form = ProfileForm()
#         return render(request, 'editProfile.html', {'form': form})
################################################---SET-PROFILE---#################################################  
    
@login_required(login_url='/users/login/')
def getProfile(request, user_name):
    profile = Profile.objects.filter(user = request.user)
    
    if not profile:
        return redirect('Set-Profile')
    
    user = get_object_or_404(User, username = user_name)
    follow_model = FollowModel.objects.filter(user = user)
    posts = Post.objects.filter(author_id = user.id)
    
    followers = list(map( lambda x:x.follower ,follow_model))
    
    liked_posts = LikesModel.objects.filter(user = request.user)
    saved_posts = SaveModel.objects.filter(user = request.user)
    post = Post.objects.aaggregate()
    
    liked = list(map(lambda x:x.post, liked_posts))
    saved = list(map(lambda x:x.post, saved_posts))
    
    print(followers)
    return render(request, 'accounts/profile.html', {'profile': user.profile, 'posts': posts, 'followers':followers, 'liked': liked, 'saved':saved})

