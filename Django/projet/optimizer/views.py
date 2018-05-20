from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponseRedirect
from django.contrib.auth.views import login
from django.http import HttpResponsePermanentRedirect
from os import path
import sys
import pandas as pd
import os
import csv

sys.path.append(path.abspath('PGPortfolio'))
#sys.path.append(path.abspath('../../PGPortfolio'))
from PGPortfolio.main import *

def return_style():
    return "html{position:relative;min-height:100%}body{overflow-x:hidden}body.sticky-footer{margin-bottom:56px}body.sticky-footer .content-wrapper{min-height:calc(100vh - 56px - 56px)}body.fixed-nav{padding-top:56px}.content-wrapper{min-height:calc(100vh -56px);padding-top:1rem}.scroll-to-top{position:fixed;right:15px;bottom:3px;display:none;width:50px;height:50px;text-align:center;color:#fff;background:rgba(52,58,64,.5);line-height:45px}.scroll-to-top:focus,.scroll-to-top:hover{color:#fff}.scroll-to-top:hover{background:#343a40}.scroll-to-top i{font-weight:800}.smaller{font-size:.7rem}.o-hidden{overflow:hidden!important}.z-0{z-index:0}.z-1{z-index:1}#mainNav .navbar-collapse{overflow:auto;max-height:75vh}#mainNav .navbar-collapse .navbar-nav .nav-item .nav-link{cursor:pointer}#mainNav .navbar-collapse .navbar-sidenav .nav-link-collapse:after{float:right;content:'\f107';font-family:FontAwesome}#mainNav .navbar-collapse .navbar-sidenav .nav-link-collapse.collapsed:after{content:'\f105'}#mainNav .navbar-collapse .navbar-sidenav .sidenav-second-level,#mainNav .navbar-collapse .navbar-sidenav .sidenav-third-level{padding-left:0}#mainNav .navbar-collapse .navbar-sidenav .sidenav-second-level>li>a,#mainNav .navbar-collapse .navbar-sidenav .sidenav-third-level>li>a{display:block;padding:.5em 0}#mainNav .navbar-collapse .navbar-sidenav .sidenav-second-level>li>a:focus,#mainNav .navbar-collapse .navbar-sidenav .sidenav-second-level>li>a:hover,#mainNav .navbar-collapse .navbar-sidenav .sidenav-third-level>li>a:focus,#mainNav .navbar-collapse .navbar-sidenav .sidenav-third-level>li>a:hover{text-decoration:none}#mainNav .navbar-collapse .navbar-sidenav .sidenav-second-level>li>a{padding-left:1em}#mainNav .navbar-collapse .navbar-sidenav .sidenav-third-level>li>a{padding-left:2em}#mainNav .navbar-collapse .sidenav-toggler{display:none}#mainNav .navbar-collapse .navbar-nav>.nav-item.dropdown>.nav-link{position:relative;min-width:45px}#mainNav .navbar-collapse .navbar-nav>.nav-item.dropdown>.nav-link:after{float:right;width:auto;content:'\f105';border:none;font-family:FontAwesome}#mainNav .navbar-collapse .navbar-nav>.nav-item.dropdown>.nav-link .indicator{position:absolute;top:5px;left:21px;font-size:10px}#mainNav .navbar-collapse .navbar-nav>.nav-item.dropdown.show>.nav-link:after{content:'\f107'}#mainNav .navbar-collapse .navbar-nav>.nav-item.dropdown .dropdown-menu>.dropdown-item>.dropdown-message{overflow:hidden;max-width:none;text-overflow:ellipsis}@media (min-width:992px){#mainNav .navbar-brand{width:250px}#mainNav .navbar-collapse{overflow:visible;max-height:none}#mainNav .navbar-collapse .navbar-sidenav{position:absolute;top:0;left:0;-webkit-flex-direction:column;-ms-flex-direction:column;flex-direction:column;margin-top:56px}#mainNav .navbar-collapse .navbar-sidenav>.nav-item{width:250px;padding:0}#mainNav .navbar-collapse .navbar-sidenav>.nav-item>.nav-link{padding:1em}#mainNav .navbar-collapse .navbar-sidenav>.nav-item .sidenav-second-level,#mainNav .navbar-collapse .navbar-sidenav>.nav-item .sidenav-third-level{padding-left:0;list-style:none}#mainNav .navbar-collapse .navbar-sidenav>.nav-item .sidenav-second-level>li,#mainNav .navbar-collapse .navbar-sidenav>.nav-item .sidenav-third-level>li{width:250px}#mainNav .navbar-collapse .navbar-sidenav>.nav-item .sidenav-second-level>li>a,#mainNav .navbar-collapse .navbar-sidenav>.nav-item .sidenav-third-level>li>a{padding:1em}#mainNav .navbar-collapse .navbar-sidenav>.nav-item .sidenav-second-level>li>a{padding-left:2.75em}#mainNav .navbar-collapse .navbar-sidenav>.nav-item .sidenav-third-level>li>a{padding-left:3.75em}#mainNav .navbar-collapse .navbar-nav>.nav-item.dropdown>.nav-link{min-width:0}#mainNav .navbar-collapse .navbar-nav>.nav-item.dropdown>.nav-link:after{width:24px;text-align:center}#mainNav .navbar-collapse .navbar-nav>.nav-item.dropdown .dropdown-menu>.dropdown-item>.dropdown-message{max-width:300px}}#mainNav.fixed-top .sidenav-toggler{display:none}@media (min-width:992px){#mainNav.fixed-top .navbar-sidenav{height:calc(100vh - 112px)}#mainNav.fixed-top .sidenav-toggler{position:absolute;top:0;left:0;display:flex;-webkit-flex-direction:column;-ms-flex-direction:column;flex-direction:column;margin-top:calc(100vh - 56px)}#mainNav.fixed-top .sidenav-toggler>.nav-item{width:250px;padding:0}#mainNav.fixed-top .sidenav-toggler>.nav-item>.nav-link{padding:1em}}#mainNav.fixed-top.navbar-dark .sidenav-toggler{background-color:#212529}#mainNav.fixed-top.navbar-dark .sidenav-toggler a i{color:#adb5bd}#mainNav.fixed-top.navbar-light .sidenav-toggler{background-color:#dee2e6}#mainNav.fixed-top.navbar-light .sidenav-toggler a i{color:rgba(0,0,0,.5)}body.sidenav-toggled #mainNav.fixed-top .sidenav-toggler{overflow-x:hidden;width:55px}body.sidenav-toggled #mainNav.fixed-top .sidenav-toggler .nav-item,body.sidenav-toggled #mainNav.fixed-top .sidenav-toggler .nav-link{width:55px!important}body.sidenav-toggled #mainNav.fixed-top #sidenavToggler i{-webkit-transform:scaleX(-1);-moz-transform:scaleX(-1);-o-transform:scaleX(-1);transform:scaleX(-1);filter:FlipH;-ms-filter:FlipH}#mainNav.static-top .sidenav-toggler{display:none}@media (min-width:992px){#mainNav.static-top .sidenav-toggler{display:flex}}body.sidenav-toggled #mainNav.static-top #sidenavToggler i{-webkit-transform:scaleX(-1);-moz-transform:scaleX(-1);-o-transform:scaleX(-1);transform:scaleX(-1);filter:FlipH;-ms-filter:FlipH}.content-wrapper{overflow-x:hidden;background:#fff}@media (min-width:992px){.content-wrapper{margin-left:250px}}#sidenavToggler i{font-weight:800}.navbar-sidenav-tooltip.show{display:none}@media (min-width:992px){body.sidenav-toggled .content-wrapper{margin-left:55px}}body.sidenav-toggled .navbar-sidenav{width:55px}body.sidenav-toggled .navbar-sidenav .nav-link-text{display:none}body.sidenav-toggled .navbar-sidenav .nav-item,body.sidenav-toggled .navbar-sidenav .nav-link{width:55px!important}body.sidenav-toggled .navbar-sidenav .nav-item:after,body.sidenav-toggled .navbar-sidenav .nav-link:after{display:none}body.sidenav-toggled .navbar-sidenav .nav-item{white-space:nowrap}body.sidenav-toggled .navbar-sidenav-tooltip.show{display:flex}#mainNav.navbar-dark .navbar-collapse .navbar-sidenav .nav-link-collapse:after{color:#868e96}#mainNav.navbar-dark .navbar-collapse .navbar-sidenav>.nav-item>.nav-link{color:#868e96}#mainNav.navbar-dark .navbar-collapse .navbar-sidenav>.nav-item>.nav-link:hover{color:#adb5bd}#mainNav.navbar-dark .navbar-collapse .navbar-sidenav>.nav-item .sidenav-second-level>li>a,#mainNav.navbar-dark .navbar-collapse .navbar-sidenav>.nav-item .sidenav-third-level>li>a{color:#868e96}#mainNav.navbar-dark .navbar-collapse .navbar-sidenav>.nav-item .sidenav-second-level>li>a:focus,#mainNav.navbar-dark .navbar-collapse .navbar-sidenav>.nav-item .sidenav-second-level>li>a:hover,#mainNav.navbar-dark .navbar-collapse .navbar-sidenav>.nav-item .sidenav-third-level>li>a:focus,#mainNav.navbar-dark .navbar-collapse .navbar-sidenav>.nav-item .sidenav-third-level>li>a:hover{color:#adb5bd}#mainNav.navbar-dark .navbar-collapse .navbar-nav>.nav-item.dropdown>.nav-link:after{color:#adb5bd}@media (min-width:992px){#mainNav.navbar-dark .navbar-collapse .navbar-sidenav{background:#343a40}#mainNav.navbar-dark .navbar-collapse .navbar-sidenav li.active a{color:#fff!important;background-color:#495057}#mainNav.navbar-dark .navbar-collapse .navbar-sidenav li.active a:focus,#mainNav.navbar-dark .navbar-collapse .navbar-sidenav li.active a:hover{color:#fff}#mainNav.navbar-dark .navbar-collapse .navbar-sidenav>.nav-item .sidenav-second-level,#mainNav.navbar-dark .navbar-collapse .navbar-sidenav>.nav-item .sidenav-third-level{background:#343a40}}#mainNav.navbar-light .navbar-collapse .navbar-sidenav .nav-link-collapse:after{color:rgba(0,0,0,.5)}#mainNav.navbar-light .navbar-collapse .navbar-sidenav>.nav-item>.nav-link{color:rgba(0,0,0,.5)}#mainNav.navbar-light .navbar-collapse .navbar-sidenav>.nav-item>.nav-link:hover{color:rgba(0,0,0,.7)}#mainNav.navbar-light .navbar-collapse .navbar-sidenav>.nav-item .sidenav-second-level>li>a,#mainNav.navbar-light .navbar-collapse .navbar-sidenav>.nav-item .sidenav-third-level>li>a{color:rgba(0,0,0,.5)}#mainNav.navbar-light .navbar-collapse .navbar-sidenav>.nav-item .sidenav-second-level>li>a:focus,#mainNav.navbar-light .navbar-collapse .navbar-sidenav>.nav-item .sidenav-second-level>li>a:hover,#mainNav.navbar-light .navbar-collapse .navbar-sidenav>.nav-item .sidenav-third-level>li>a:focus,#mainNav.navbar-light .navbar-collapse .navbar-sidenav>.nav-item .sidenav-third-level>li>a:hover{color:rgba(0,0,0,.7)}#mainNav.navbar-light .navbar-collapse .navbar-nav>.nav-item.dropdown>.nav-link:after{color:rgba(0,0,0,.5)}@media (min-width:992px){#mainNav.navbar-light .navbar-collapse .navbar-sidenav{background:#f8f9fa}#mainNav.navbar-light .navbar-collapse .navbar-sidenav li.active a{color:#000!important;background-color:#e9ecef}#mainNav.navbar-light .navbar-collapse .navbar-sidenav li.active a:focus,#mainNav.navbar-light .navbar-collapse .navbar-sidenav li.active a:hover{color:#000}#mainNav.navbar-light .navbar-collapse .navbar-sidenav>.nav-item .sidenav-second-level,#mainNav.navbar-light .navbar-collapse .navbar-sidenav>.nav-item .sidenav-third-level{background:#f8f9fa}}.card-body-icon{position:absolute;z-index:0;top:-25px;right:-25px;font-size:5rem;-webkit-transform:rotate(15deg);-ms-transform:rotate(15deg);transform:rotate(15deg)}@media (min-width:576px){.card-columns{column-count:1}}@media (min-width:768px){.card-columns{column-count:2}}@media (min-width:1200px){.card-columns{column-count:2}}.card-login{max-width:25rem}.card-register{max-width:40rem}footer.sticky-footer{position:absolute;right:0;bottom:0;width:100%;height:56px;background-color:#e9ecef;line-height:55px}@media (min-width:992px){footer.sticky-footer{width:calc(100% - 250px)}}@media (min-width:992px){body.sidenav-toggled footer.sticky-footer{width:calc(100% - 55px)}}"
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
    style = return_style()
    return render(request, 'optimizer/dashboard.html', locals())
def optimize(request):
    style = return_style()
    algorithms = ['Neural Network', 'anticor1', 'bcrp', 'best', 'bk', 'cornk', 'crp', 'cwmr_std', 'eg', 'm0', 'olmar', 'olmar2', 'pamr', 'rmr', 'sp', 'ubah', 'up', 'wmamr']
    number_algorithms = len(algorithms)
    return render(request, 'optimizer/optimize.html', locals())

def pgportfolio(request, query=None):
    style = return_style()
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
    style = return_style()
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

def url_redirect(request):
    return HttpResponsePermanentRedirect("/accounts/login/")
