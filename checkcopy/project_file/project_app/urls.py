"""project_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
import posts.views
from django.urls import re_path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',posts.views.home_page,name="home"),
    path('admin/', admin.site.urls),
    path('create/',posts.views.posts_create,name="create"),
    re_path(r'^(?P<id>\d+)/$',posts.views.posts_detail,name="post_detail"),
    path('list/',posts.views.posts_list,name="list"),
    re_path(r'^(?P<id>\d+)/edit/$',posts.views.posts_update,name="update"),
    re_path(r'^(?P<id>\d+)/delete/$',posts.views.posts_delete,name="delete"),
    path('login/',posts.views.login_page,name="login"),
    path('logout/',posts.views.logout_page,name="logout"),
    path('register/',posts.views.register_page,name="register"),
    path('userpage/',posts.views.user_page,name="userpage"),
    path('userlist/',posts.views.user_list,name="userlist"),
    path('about/',posts.views.about,name="about"),
    path('commposts/',posts.views.commented_posts,name="commposts"),
]

if(settings.DEBUG):
    urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
