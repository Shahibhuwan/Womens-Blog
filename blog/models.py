from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
# Create your models here.

default_id =1


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    image= models.ImageField( upload_to="profile/" ,null=True)
    phone= models.CharField( max_length=50, null=True)
    profession =models.CharField(max_length=100 ,null=True)
    currently_working = models.CharField(max_length=100,null=True) 


#profile class for update profile
class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    def save(self, *args, **kwargs):
        self.slug =slugify(self.title)
        super(Category, self).save(*args, **kwargs)


    def __str__(self):
        return self.title
class Post(models.Model):
    customer=models.CharField(max_length=100, null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE ,default=default_id)
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to="post/", null=True)
    views_count=models.PositiveIntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug =slugify(self.title)
        super(Post, self).save(*args, **kwargs)
