from django.urls import path, re_path
from . import views
from django.contrib import admin
from django.urls import path, include

# comme ça on peut passer l'url "optimizer/article/42"
urlpatterns = [
    path('dashboard.html', views.dashboard),
    path('login.html', views.login),
    path('optimize.html', views.optimize),
]
