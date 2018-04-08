from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponseRedirect

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
