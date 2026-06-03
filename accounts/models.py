from django.db import models
from django.contrib.auth.models import User
import os, datetime

def getFileName(instance, filename):
    time = datetime.datetime.now().strftime('%d-%m-%y %H-%M-%S')
    new_filename = '%s%s'%(time,filename)
    out = os.path.join('uploads', new_filename)
    print(out)
    return out

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.CharField(max_length=250, null=False, blank=True)
    profileImage = models.ImageField(upload_to=getFileName,  null=False, blank=True)
    followers = models.IntegerField(default=0,null=False, blank=False)
    following = models.IntegerField(default=0,null=False, blank=False)
    posts = models.IntegerField(default=0,null=False, blank=False)
    
    
    def __str__(self):
        return self.user.username