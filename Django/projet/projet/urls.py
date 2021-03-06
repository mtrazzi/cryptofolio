"""projet URL Configuration

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
from django.conf.urls import url
from django.conf.urls import include
from registration.backends.default.views import RegistrationView
from registration.forms import RegistrationForm
from django.views.generic.base import RedirectView
from optimizer import views

# ajouter toutes nos pages (i.e. fonctions) à cette list
urlpatterns = [
    url('admin/', admin.site.urls),
    #path('accounts/', include('django.contrib.auth.urls')),
    #path('accounts/', include('optimizer.urls')),
    url('optimizer/', include('optimizer.urls')),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^.*$', views.url_redirect, name="url-redirect")
]
