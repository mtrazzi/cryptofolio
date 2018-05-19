from django.urls import path, re_path
from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

urlpatterns = [
    path('dashboard.html', views.dashboard),
    #path('login.html', views.login),
    #path('register.html', views.register),
    path('optimize.html', views.optimize),
    path('pgportfolio.html', views.pgportfolio),
    path('portfolios.html', views.portfolios),
    url(r'^portfolio/(?P<query>\w+)$', views.pgportfolio),
]
