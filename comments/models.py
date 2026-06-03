from django.db import models
from blog.models import Post
from django.contrib.auth.models import User
import uuid

# Create your models here.
class CommentsModel(models.Model):
    content = models.TextField()
    
    blog = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    cmnt_idx = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='replies'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} - {self.content[:20]}"