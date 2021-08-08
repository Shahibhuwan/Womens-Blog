from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.



EXPERIENCE_CHOICES = (
    ('BEGINNER','BEGINNER'),
    ('MID', 'MID'),
    ('EXPERT','EXPERT')
)
AVAILABILITY_CHOICES =(('1','1'),
('2','2'),
('3','3'),
('3+','3+')

)
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    def __str__(self):
        return self.full_name



class Publisher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    rating = models.IntegerField(default=1, validators=[MaxValueValidator(10),MinValueValidator(1)])
    def __str__(self):
        return self.full_name


class Profile(models.Model):
    customer =models.OneToOneField(Customer, on_delete=models.CASCADE, null=True)
    description = models.TextField(verbose_name="you can write about yourself")
    secondary_email =models.EmailField(max_length=100, unique=True)
    image = models.ImageField(upload_to="profile")
    
    phone= models.CharField( max_length=50 )
    profession =models.CharField(max_length=100)
    currently_working = models.CharField(max_length=100)
    experience = models.CharField(max_length=10, choices=EXPERIENCE_CHOICES, default='BEGINNER')
    hourtly_rate= models.PositiveIntegerField(default=2)
    total_projects =models.PositiveIntegerField(default=0)
    english_level=models.CharField(max_length=10, choices=EXPERIENCE_CHOICES, default='BEGINNER')
    availability=models.CharField(max_length=10, choices=AVAILABILITY_CHOICES, default='1')
    
    def __str__(self):
        return self.customer.full_name

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
    publisher=models.ForeignKey(Publisher, on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    #description = models.TextField()
    #description = RichTextField(blank=Ture)
    description = RichTextUploadingField(blank=True, config_name='special')
    #description = RichTextUploadingField(blank=True, config_name='special',external_plugin_resources=[('youtube','/static/blog/ckeditor/ckeditor_plugins/youtube/youtube/','plugin.js')])
    image = models.ImageField(upload_to="post")
    views_count=models.PositiveIntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug =slugify(self.title)
        super(Post, self).save(*args, **kwargs)
    

class Readedarticle(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    view_counts=models.PositiveIntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
# one post have 1tomany readed article 
    def __str__(self):
        return self.customer.full_name

class Contact(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField(unique=True)
    message= models.TextField()

    def __str__(self) :
        
        return self.contact

class Subscribe(models.Model):
    email= models.EmailField(unique=True)

