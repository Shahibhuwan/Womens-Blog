from blog.models import Category, Post
from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register([Post, Category,Customer,Profile, Readedarticle,Publisher,Contact,Subscribe])