"""cherrytea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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

from cherrytea_app.views import *

urlpatterns = [
    path('', index, name='index'),
    path('home/', home, name='home'),
    path('browse/', browse, name='browse'),
    path('group/<int:id>/', group, name='group'),
    path('group/<int:id>/plan/', create_plan, name='create_plan'),
    path('user/plans/<int:id>/', plan, name='plan'),

    path('user/plans/<int:id>/cancel/', cancel_plan),
    path('signin/', sign_in,),
    path('signup/', sign_up),
    path('signout/', sign_out),

    path('admin/', admin.site.urls),
]
