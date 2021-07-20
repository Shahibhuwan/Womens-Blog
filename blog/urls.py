from blog.models import Customer
from django.urls import path
from .views import *
app_name='blog'
urlpatterns = [
    path('',HomeView.as_view(), name="home"),
    path('health/',HealthView.as_view(), name="health"),
    path('singlepost/<slug:slug>/',SinglePostView.as_view(), name="singlepost"),
    path('customer-registration/',CustomerRegistration.as_view(), name="customerregistration" )
]
