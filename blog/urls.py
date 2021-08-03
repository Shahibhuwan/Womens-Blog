from django.urls import include
from blog.models import Customer
from django.urls import path
from .views import *
app_name='blog'
urlpatterns = [
    path('',HomeView.as_view(), name="home"),
    path('health/',HealthView.as_view(), name="health"),
    path('singlepost/<slug:slug>/',SinglePostView.as_view(), name="singlepost"),
    path('customer-registration/',CustomerRegistration.as_view(), name="customerregistration" ),
    path('accounts/login/',CustomerLogin.as_view(),name='customerlogin'),
    path("customer-profile/", CustomerProfile.as_view(), name= "customerprofile"),
    path('customer-logout/',CustomerLogout.as_view(), name='customerlogout'),
    path('profile-edit/<pk>', ProfileEdit.as_view(),name='profileedit' ),
    path('profile-add/',ProfileAdd.as_view(),name='profileadd' ),
    path('lifestylebeauty/',LifestyleBeautyView.as_view(), name="lifestylebeauty"),
    path('lifestylefashion/',LifestyleFashionView.as_view(), name="lifestylefashion"),
    path('culture/',CultureView.as_view(), name="culture"),
    path('motherhood/',MotherhoodView.as_view(), name="motherhood"),
    path('travel/',TravelView.as_view(), name="travel"),
    path('contact/',ContactView.as_view(),name="contact"),
    path('about/',AboutView.as_view(), name="about"),
    path('publishpost/',PublishPost.as_view(), name="publishpost"),
    path('forgot-password/',ForgotPasswordView.as_view(),name="forgotpassword"),
    path("password-reset/<email>/<token>/",PasswordResetView.as_view(), name="passwordreset"),
    path("subscribe/",SubscribeView.as_view(), name="subscribe"),
    
    
]
