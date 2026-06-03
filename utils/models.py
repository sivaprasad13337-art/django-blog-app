from django.db import models
from blog.models import Post
from accounts.models import User

# Create your models here.
class LikesModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    
    class Meta:
        unique_together = ('user', 'post')
        

class SaveModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    
    class Meta:
        unique_together = ('user', 'post')
        
        
class FollowModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    
    class Meta:
        unique_together = ('user', 'follower')