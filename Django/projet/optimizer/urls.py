from . import views
from django.contrib import admin
from django.conf.urls import include
from django.conf.urls import url

urlpatterns = [
    url('dashboard.html', views.dashboard),
    url('optimize.html', views.optimize),
    url('pgportfolio.html', views.pgportfolio),
    url('portfolios.html', views.portfolios),
    url(r'^portfolio/(?P<query>\w+)$', views.pgportfolio),
]
