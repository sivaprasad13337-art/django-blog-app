from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .form import CommentsForm
from .models import CommentsModel
from blog.models import Post
import datetime

# Create your views here.
@login_required(login_url='/users/login/')
def getComments(request):
    comments = [{'user': 'Harry', 'comment':'Cool:)'},{'user': 'Nicol', 'comment':"that's interesting!"},{'user': 'Jessica', 'comment':'❤️‍🔥'}, ]
    form = CommentsForm()
    return render(request, 'comment_section.html',{'comments':comments, 'form': form})


@login_required(login_url='/users/login/')
def add_Comment(request, blog_id, parent_id):
    blog = get_object_or_404(Post, id=blog_id)
    parent = None
    if parent_id:
        parent = get_object_or_404(CommentsModel, id = parent_id)
        
    if request.method == 'POST':
        form = CommentsForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.blog = blog
            comment.parent = parent
            comment.save()
            return redirect('GET-BLOG', slug=blog.slug)
    else:
        return redirect('GET-BLOG', slug=blog.slug)
    
@login_required(login_url='/users/login/')
def delete_comment(request, id, blog_id):
    comment = get_object_or_404(CommentsModel, id = id)
    blog = get_object_or_404(Post, id = blog_id)
    
    if request.user == comment.user:
        comment.delete()
        return redirect('GET-BLOG', slug=blog.slug)
    else:
        return render(request, 'comment_section.html', {'error': "you can't delete this comment"})
    