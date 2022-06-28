from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

class User(AbstractUser):
    email=models.EmailField(unique=True)
    mobile=models.CharField(max_length=15)
    profile_pic=models.FileField(upload_to='profile',default='1.png')
    bio=models.TextField(max_length=200)
    friends=models.ManyToManyField('User')
    
    def __str__(self):
       return self.username +'-'+ self.email
   
    @property
    def total_friends(self):
        return self.friends.count()
    
class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    files=models.FileField(upload_to='post')
    dec=models.TextField(max_length=200)
    date=models.DateField(default=datetime.date.today)
    likes=models.ManyToManyField(User,related_name="post_like")
    
    def __str__(self):
       return self.user.username 
   
    @property
    def total_likes(self):
        return self.likes.count()
    
    
    
class Comment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    comment=models.CharField(max_length=100)
    date=models.DateTimeField(auto_now_add=True) 
    
     
    def __str__(self):
        return self.user.username
     
    
class Friendrequest(models.Model):
    to_user=models.ForeignKey(User,related_name='to_user',on_delete=models.CASCADE)
    from_user=models.ForeignKey(User,related_name='from_user',on_delete=models.CASCADE)
    date_time=models.DateTimeField(auto_now_add=True)
    status=models.BooleanField(default=False)      
       
    def __str__(self):
        return self.to_user.username
       
    
    