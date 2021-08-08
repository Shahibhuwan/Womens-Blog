"""womenblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.urls.conf import include
from ckeditor_uploader import views
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
   # path("ckeditor/", include("ckeditor_uploader.urls")),
    url(r'^ckeditor/upload/', login_required(views.upload), name='ckeditor_upload'),
    url(r'^ckeditor/browse/', never_cache(login_required(views.browse)), name='ckeditor_browse'),
    path('accounts/', include('allauth.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# This is happening because the default urls are decorated with @staff_member_required(https://github.com/django-ckeditor/django-ckeditor/blob/master/ckeditor_uploader/urls.py). To avoid this, instead of including the urls like so url(r'^ckeditor/', include('ckeditor_uploader.urls')) you could define them one by one in your urls.py with the login_required decorator: