

def verify_views(request, post):
    viewed_posts = request.session.get('viewed_posts', [])
    
    if post.id not in viewed_posts:
        post.views += 1
        post.save()
        viewed_posts.append(post.id)
        request.session['viewed_posts'] = viewed_posts
        
    return True