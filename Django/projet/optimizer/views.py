from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponseRedirect
from django.contrib.auth.views import login
from os import path
import sys
import pandas as pd
import os
import csv

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
def optimize(request):
    algorithms = ['Neural Network', 'anticor1', 'bcrp', 'best', 'bk', 'cornk', 'crp', 'cwmr_std', 'eg', 'm0', 'olmar', 'olmar2', 'pamr', 'rmr', 'sp', 'ubah', 'up', 'wmamr']
    number_algorithms = len(algorithms)
    return render(request, 'optimizer/optimize.html', locals())

def pgportfolio(request, query=None):
    name = request.GET['name']
    algo = request.GET['algorithm']
    labels = ['Neural Network', 'anticor1', 'bcrp', 'best', 'bk', 'cornk', 'crp', 'cwmr_std', 'eg', 'm0', 'olmar', 'olmar2', 'pamr', 'rmr', 'sp', 'ubah', 'up', 'wmamr']
    real_name = ['8', 'anticor1', 'bcrp', 'best', 'bk', 'cornk', 'crp', 'cwmr_std', 'eg', 'm0', 'olmar', 'olmar2', 'pamr', 'rmr', 'sp', 'ubah', 'up', 'wmamr']
    dic3 = dict(zip(labels, real_name))
    algo_to_use = dic3[algo]
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
    portfolio, omega = process(algo_to_use)
    coins = ['BTC', 'USDT', 'ETH', 'XRP', 'STR', 'XMR', 'LTC', 'BCH', 'DASH', 'BTS', 'XEM', 'ETC']
    dic = dict(zip(coins, omega))
    dic2 = dict(zip(coins, portfolio))
    weights = sorted(dic.items(), key=lambda x: x[1], reverse=True)
    for i in range (len(omega)):
        omega[i] = (int(omega[i])) #delete useless digits and make int
    request.session["portfolio"] = dic2
    request.session["portfolio_name"] = name
    request.session["chart"] = dic
    return render(request, 'optimizer/result.html', locals())

def portfolios(request, query=None):
    print("hello")
    f = open('portfolios.csv', 'a+')
    if ('portfolio_name' in request.session and not "delete" in request.GET and "saved" in request.GET):
        # Saving portfolio
        print("saving")
        l = [0]*12 #list with our portfolio to save
        l[0] = request.user.username
        l[1] = request.session["portfolio_name"]
        l[2:12] = request.session["portfolio"].values()
        print("to save: ", l)
        #wr = csv.writer(f)
        #wr.writerow(l)
        str_list = [str(x) for x in l]
        print(",".join(str_list), file=f)
    f.close()

    f2 = open('portfolios.csv', 'r')
    reader = csv.reader(f2)
    myset = set()
    for row in reader:
        print("type", type(row))
        myset.add(tuple(row))
    portfolios_list = [list(x) for x in myset]
    print("type", type(reader))
    truc = tuple(reader)
    print("truc", truc)
    print(portfolios_list)

    # Deleting portfolio from get button
    if ("delete" in request.GET):
        print("deleting")
        name = request.GET["delete"]
        to_del = []
        for i in range (len(portfolios_list)):
            if (portfolios_list[i][0] == request.user.username
            and portfolios_list[i][1] == name):
                to_del.append(i)
        for index in reversed(to_del):
            del portfolios_list[index]
    print(portfolios_list)
    #os.system("sort -u -t, -k1,2 portfolios.csv &> unique.csv")
    #os.system("rm portfolios.csv")
    #os.system("cp unique.csv portfolios.csv
    # Creating dictionary to pass to views
    with open("portfolios.csv", 'w') as f:
        f.truncate(0)
        for row in portfolios_list:
            print(",".join(row), file=f)
    dic = {}
    dic_keys = ['BTC','USDT','ETH','XRP','STR','XMR','LTC','BCH','DASH','BTS','XEM','ETC']
    for row in portfolios_list:
        if (row[0] == request.user.username):
            dic[row[1]] = {}
            d = dict(zip(dic_keys, np.array(row[2:14])))
            for key, value in d.items():
                if float(value) > 0.0:
                    dic[row[1]][key] = value
    dic3 = {}
    dic3 = request.session["chart"]
    print(dic)
    return render(request, 'optimizer/portfolios.html', locals())
