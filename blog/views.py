from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.http import request
from django.conf import settings
from django.urls.base import reverse
from .utils import password_reset_token
from django.core.mail import send_mail
from django.utils.translation import templatize
from blog.forms import ContactForm, CreatePostForm, EditProfileForm, ForgotPasswordForm, PasswordResetForm, UserRegistration,LoginForm
from django.shortcuts import redirect, render
from django.views.generic.base import RedirectView, TemplateView, View
from django.views.generic import DetailView
from .models import Category, Contact, Customer, Post,Profile, Publisher, Readedarticle, Subscribe
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class HomeView(TemplateView):
    template_name= "index.html"
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        
        context['popular'] = Post.objects.filter(views_count__gt=20 ).order_by("-id")[0:3]
        context['recent'] =Post.objects.all().order_by("-id")[0:3]
        context['latest']= Post.objects.latest('id')
        return context

class HealthView(TemplateView):
    template_name="health.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(title='Health')
        
        all_post = category.post_set.all().order_by("-id")
        paginator = Paginator(all_post,2)
        page_number =self.request.GET.get("page")
        post_list = paginator.get_page(page_number)
        context['post_list'] = post_list
        context['mostread'] = category.post_set.filter(views_count__gt=10).order_by("-id")[:5]
        return context

class LifestyleFashionView(TemplateView):
    template_name="lifestylefashion.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(title='LifestyleFashion')
        
        all_post = category.post_set.all().order_by("-id")
        paginator = Paginator(all_post,5)
        page_number =self.request.GET.get("page")
        post_list = paginator.get_page(page_number)
        context['post_list'] = post_list
        context['mostread'] = category.post_set.filter(views_count__gt=10).order_by("-id")[:5]
        return context

class LifestyleBeautyView(TemplateView):
    template_name="lifestylebeauty.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(title='LifestyleBeauty')
        
        all_post = category.post_set.all().order_by("-id")
        paginator = Paginator(all_post,5)
        page_number =self.request.GET.get("page")
        post_list = paginator.get_page(page_number)
        context['post_list'] = post_list
        context['mostread'] = category.post_set.filter(views_count__gt=10).order_by("-id")[:5]
        return context

class CultureView(TemplateView):
    template_name="culture.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(title='Culture')
        
        all_post = category.post_set.all().order_by("-id")
        paginator = Paginator(all_post,5)
        page_number =self.request.GET.get("page")
        post_list = paginator.get_page(page_number)
        context['post_list'] = post_list
        context['mostread'] = category.post_set.filter(views_count__gt=10).order_by("-id")[:5]
        return context


class TravelView(TemplateView):
    template_name="travel.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(title='Travel')
        
        all_post = category.post_set.all().order_by("-id")
        paginator = Paginator(all_post,5)
        page_number =self.request.GET.get("page")
        post_list = paginator.get_page(page_number)
        context['post_list'] = post_list
        context['mostread'] = category.post_set.filter(views_count__gt=10).order_by("-id")[:5]
        return context
class MotherhoodView(TemplateView):
    template_name="Motherhood.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(title='Motherhood')
        
        all_post = category.post_set.all().order_by("-id")
        paginator = Paginator(all_post,5)
        page_number =self.request.GET.get("page")
        post_list = paginator.get_page(page_number)
        context['post_list'] = post_list
        context['mostread'] = category.post_set.filter(views_count__gt=10).order_by("-id")[:5]
        return context
class ContactView(CreateView):
    template_name ="contact.html"
    form_class = ContactForm
    success_url=reverse_lazy('blog:contact')
    model = Contact
    
class SinglePostView(DetailView):
    template_name ='single.html'
    model = Post
    context_object_name = 'post'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug=self.kwargs.get('slug')
        post =Post.objects.get(slug=slug)
        post.views_count+=1
        post.save()
        category_title = post.category.title
        context['single']=post
       
        user = self.request.user
        # checking existing readed article and adding in linking this article with user/customer
        if self.request.user.is_authenticated:
            readed_article = Readedarticle.objects.filter(Q(customer=user.customer) & Q(post=post))
            if readed_article:
           
                view_count =Readedarticle.objects.get(Q(customer=user.customer) & Q(post=post))
                view_count.view_counts+=1
                view_count.save()
            else:
           
                readed_article = Readedarticle(customer=user.customer,view_counts=1, post = post)
                readed_article.save()
        category = Category.objects.get(title=category_title)
        similar =category.post_set.all()[:3]
        context['similar'] = similar
        return context
    

class CustomerRegistration(CreateView):
    form_class= UserRegistration
    template_name ='register.html'
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

class CustomerLogout(View):
    def get(self, request):
        logout(self.request)
        return redirect(reverse_lazy('blog:home'))





class PublishPost(LoginRequiredMixin,CreateView):
    model= Post
    template_name="publisher/createpost.html"
    form_class = CreatePostForm
    success_url=reverse_lazy("blog:home")

    #customer ko satta publisher rakhne post model ma and rating ko lagi publisheko model vitra euta field banaune 
    def form_valid(self, form):
        user=self.request.user
        form.instance.publisher = user.publisher

        form.save()
        return super().form_valid(form)

    



class CustomerLogin(FormView):
    template_name="login.html"
    form_class=LoginForm
    success_url=reverse_lazy("blog:home")


    def form_valid(self, form):
        username=form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(username=username, password=password)
        if user:
            login( self.request, user)
        else: 
            
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid credentials"})
        return super().form_valid(form)
        # redirect ma feri login ma lagne and model admin set agarne ra home page ko bg image and data intyr

class CustomerProfile(LoginRequiredMixin,TemplateView):
    template_name="portfolio.html"
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        user = self.request.user
        #for customer profile detail
        if Customer.objects.filter(user=user).exists():
            context['customer']= user.customer
            customer =Customer.objects.get(user= user)
            articles = Readedarticle.objects.filter(customer =customer )
            context['articles']= articles
        else:
            context['customer']=None
        
        
   #for readed article
   # use query parameter viewcount to get most readed article of user
        
        return context
            
  

class ProfileAdd(LoginRequiredMixin,CreateView):
    template_name= "addprofile.html"
    model =Profile
    form_class =EditProfileForm
    success_url=reverse_lazy("blog:customerprofile")

   

    def form_valid(self, form):
        customer = self.request.user.customer
        form.instance.customer =customer
        return super().form_valid(form)

    
    
class ProfileEdit(LoginRequiredMixin,UpdateView):
    model =Profile
    template_name= "editprofile.html"
    form_class =EditProfileForm
    success_url=reverse_lazy("blog:customerprofile")



class ForgotPasswordView(FormView):
    template_name = "forgotpassword.html"
    form_class=ForgotPasswordForm
    success_url ='/forgot-password/?m=s'

    def form_valid(self, form):
        # get the email for user
        email = form.cleaned_data.get("email")

        # get the current host ip/domain
        url = self.request.META['HTTP_HOST']
        # get custmer and then user
        customer = Customer.objects.get(user__email =email) 
        user= customer.user
        #generate and send mail to the user with email
        text_content ='Please Click the link below to reset your password  '
        html_content = url + "/password-reset/" + email + \
            "/" + password_reset_token.make_token(user) + "/"
        send_mail(
            'Password Reset Link | Django Ecommerce',
            text_content + html_content,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        return super().form_valid(form)



        

class PasswordResetView(FormView):
    template_name = "passwordreset.html"
    form_class = PasswordResetForm
    success_url = "/customer-login/"
#order flow:dispatch, cleaned field level validation and form valid
    def dispatch(self, request, *args, **kwargs):
        email = self.kwargs.get("email")
        user = User.objects.get(email=email)
        token = self.kwargs.get("token")
        if user is not None and password_reset_token.check_token(user, token):
            pass
        else:
            return redirect(reverse("ecomapp:passworforgot") + "?m=e")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        password = form.cleaned_data['new_password']
        email = self.kwargs.get("email")
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        return super().form_valid(form)    


class AboutView(TemplateView):
    template_name="about.html"

class SubscribeView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'blog:home'

    def get_redirect_url(self, *args, **kwargs):
        # user =request.user
        # customer = user.customer
        email = self.request.POST['email']
        subscribe = Subscribe.objects.create( email=email)
        subscribe.save()
        return super().get_redirect_url(*args, **kwargs)


