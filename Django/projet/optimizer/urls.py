from django.urls import path, re_path
from . import views

# comme ça on peut passer l'url "optimizer/article/42"
urlpatterns = [
    re_path(r'^accueil/', views.home),
    re_path(r'^article/(?P<id_article>.+)/', views.view_article),
    path('date/', views.date_actuelle),
    path('addition/<int:nombre1>/<int:nombre2>/', views.addition),
    path('landingpage/', views.landingpage),
    path('githubrepo/', views.githubrepo),
    path(r'^dashboard/', views.dashboard),
]
