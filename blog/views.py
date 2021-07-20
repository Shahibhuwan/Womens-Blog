from django.contrib.auth.models import User
from blog.forms import UserRegistration
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import DetailView
from .models import Category, Customer, Post
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
# Create your views here.

class HomeView(TemplateView):
    template_name= "index.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['popular'] = Post.objects.filter(views_count__gt=20 )[0:3]
        context['recent'] =Post.objects.all().order_by("-id")[0:3]
        context['latest']= Post.objects.latest('id')
        return context

class HealthView(TemplateView):
    template_name="health.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(title='Health')
        
        context['category'] = category
        context['mostread']=Post.objects.filter(category= category, views_count__gt=10)
        
        return context


class SinglePostView(DetailView):
    template_name='single.html'
    model=Post
    context_object_name= 'post'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug=self.kwargs.get('slug')
        post =Post.objects.get(slug=slug)
        post.views_count=+1
        post.save()

         
        return context
    
class CustomerRegistration(CreateView):
    form_class= UserRegistration
    template_name ='customerregistation.html'
    model = Customer
    success_url =reverse_lazy('blog:home')

    def form_valid(self, form):
        username= form.cleaned_data.get("username")
        password= form.cleaned_data.get("password")
        email= form.cleaned_data.get("email")
        
        user = User.objects.create_user(username,email,password)
        form.instance.user=user
        login(self.request,user)
        return super().form_valid(form)