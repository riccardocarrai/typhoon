from django.shortcuts import render
from django.db import models
from django.template import loader, Context, RequestContext
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from catalogo.models  import *
from prodotti.models import *
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from catalogo.media import media
import re

# Create your views here
def index(request):
    #page = loader.get_template('index.html')
    #t = UnionQuery()
    request.session['categorie']=UnionQuery()
    pr_ev=Prodotto.objects.filter(in_evidenza="true").values('prodotto','prodotto_new','sconto_globale')
    cat_ev = categoria.objects.filter(in_evidenza="true").values('categoria','small_image')
    slider=media.objects.filter(pagina='index',tipo='1').values('titolo','image','didascalia','url')
    adv=media.objects.filter(pagina='index',tipo='2').values('image','url')
    #if request.user.is_authenticated():
        #user_name=request.user.get_full_name()
        #auth=True
    #else:
        #auth=False
        #user_name=''
    #c = Context({'categorie':t,
                 #'user_name':user_name,
                 #'auth':auth,
                 #'pr_ev':pr_ev,
                 #'cat_ev':cat_ev,
                 #'slider':slider,
                 #'adv':adv})
    #return HttpResponse(page.render(c))
    return render_to_response('index.html',locals())

def login(request):
    c={}
    c.update(csrf(request))
    return render_to_response('login.html', c)

def auth_view(request):
    username =request.POST.get('username','')
    password = request.POST.get('password','')
    user=auth.authenticate(username=username , password=password)
    if user is not None:
        auth.login(request, user)
        #name= request.user.get_full_name()
        request.session['name']= request.user.get_username()
        request.session['aut']=True
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')




def logoutWiews(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def categorie(request, categoria):
    rif=categoria
    # categorie=categoria.objects.all()
    return render_to_response('prodotto.html',locals())







def UnionQuery():
    mapping={}
    categorie_list=categoria.objects.values('categoria', 'prodotti')
    prodotto_list=Prodotto.objects.values('prodotto','prodotto_new','sconto_globale')
    result_list=[]
    for x in categorie_list:
        for y in prodotto_list:
            if x['prodotti']==y['prodotto']:
                mapping=x
                mapping['new']=y['prodotto_new']
                mapping['sconto']=y['sconto_globale']
                result_list.append(mapping)
    return result_list



#Prodotto.objects.values('categoria','prodotto')
