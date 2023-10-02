from django.db import models
from django.contrib.auth.models import User
from froala_editor.fields import FroalaField
from autoslug import AutoSlugField
from .helpers import *

class BlogModel(models.Model):
    title = models.CharField(max_length=1000,unique=True)
    content = FroalaField()
    slug = AutoSlugField(populate_from="title",unique=True,default=None,max_length=1000, null=True, blank=True)
    user = models.ForeignKey(User, blank=True, null=True,
                             on_delete=models.CASCADE)
   
    image = models.ImageField(upload_to='blog')
    created_at = models.DateTimeField(auto_now_add=True)
    upload_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    count1 = models.IntegerField(default=0)
    def increment_view_count2(self):
        self.count1 += 1
        self.save()
    def increment_view_count(self):
        self.views += 1
        self.save()


    def __str__(self):
        return self.title
class Bloggers(models.Model):
    name = models.CharField(max_length=1000)
    
    blogs = models.ManyToManyField(BlogModel, related_name='bloggers')
    category = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

class Profile(models.Model):
    Name = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    img = models.ImageField(blank=True)
    facebook = models.CharField(max_length=1000)
    instagram = models.CharField(max_length=1000)
    about = models.TextField()

class Addcomment(models.Model):
    name =  models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    blog = models.ForeignKey(BlogModel,related_name="comments", on_delete=models.CASCADE)
    comment = models.TextField(default=None) 
    time = models.DateTimeField(auto_now_add=True)
   


    def __str__(self):
        return self.blog.title

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.message}'
