from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponseRedirect
from django.contrib.auth.views import login
from os import path
import sys

sys.path.append(path.abspath('PGPortfolio'))
#sys.path.append(path.abspath('../../PGPortfolio'))
from PGPortfolio.main import *


# Fonction home
#request = info sur la méthode de requète (get ou post) et autres
def home(request):
    return render(request, 'optimizer/accueil.html', locals())

def view_article(request, id_article):
    """
    Vue qui affiche un article selon son identifiant (ou ID, ici un numéro)
    Son ID est le second paramètre de la fonction (pour rappel, le premier
    paramètre est TOUJOURS la requête de l'utilisateur)
    """
    return HttpResponse(
        "Vous avez demandé l'article #{0} !".format(id_article)
    )

def date_actuelle(request):
    return render(request, 'optimizer/date.html', {'date': datetime.now()})

def addition(request, nombre1, nombre2):
    total = nombre1 + nombre2
    # Retourne nombre1, nombre2 et la somme des deux au tpl
    return render(request, 'optimizer/addition.html', locals())

def landingpage(request):
    return HttpResponseRedirect('https://michaeltrazzi.wixsite.com/cryptoptimisation')

def githubrepo(request):
    return HttpResponseRedirect('https://github.com/mtrazzi/cryptofolio')

def dashboard(request):
    return render(request, 'optimizer/dashboard.html', locals())

def login(request):
    return render(request, 'optimizer/login.html', locals())

def optimize(request):
    return render(request, 'optimizer/optimize.html', locals())

def pgportfolio(request, query=None):
    name = request.GET['name']
    #risk = request.GET['risk']
    capital = request.GET['capital']
    """
    omega = main()
    for i in range (len(omega)):
        if (omega[i] <= 0.05):
            omega[i] = 0 #delete useless coins
        else:
            omega[i] = int(omega[i] * 1000)
    omega = (100/sum(omega)) * omega #normalize and transform in percent
    """
    portfolio, omega = main()
    coins = ['BTC', 'USDT', 'ETH', 'XRP', 'STR', 'XMR', 'LTC', 'BCH', 'DASH', 'BTS', 'XEM', 'ETC']
    dic = dict(zip(coins, omega))
    dic2 = dict(zip(coins, portfolio))
    weights = sorted(dic.items(), key=lambda x: x[1], reverse=True)
    for i in range (len(omega)):
        omega[i] = (int(omega[i])) #delete useless digits and make int
    return render(request, 'optimizer/result.html', locals())
