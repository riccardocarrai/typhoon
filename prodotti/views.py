# -*- coding: utf-8 -*-

from django.shortcuts import render
from prodotti.models import *
from django.views.generic import View
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render_to_response
from django.db import models
import re
from django import template
from anagrafiche.models import *
from django.core.context_processors import csrf
from django.core import serializers
import json
from decimal import *
from catalogo.media import *
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone
# Create your views here.


class ViewsProd(View):

    def ButtonImage(self,list,object,types):
        button=[]
        ob=[]
        nome=[]
        for i in list:
           #c=ProdottiImage.objects.filter(object_id=i[object], Oggetto ='Button').values('object_id','image')
           c=Immagini.objects.filter(object_id=i, Oggetto ='Button').values('object_id','image','content_type_id')
           if(c and (c[0]['content_type_id'])==types):
            c[0][object]=c[0]['object_id']
            if(ob != type(i)):
                c[0]['id']=nome
            del(c[0]['object_id'])
            button.append(c[0])
           else:
               ob=type(i)
               nome=i.nome
        return button

class ViewsCategorie(ViewsProd):

    def get(self, request, categoria):
        rif=categoria
        # categorie=categoria.objects.all()
        return render(request,'prodotto.html',locals())

class ViewsProdotti(ViewsProd):

    def get(self, request, categoria, prodotto):
        cat=categoria
        prod=re.sub('-', ' ', prodotto)
        comp=Prodotto.objects.get(prodotto__iexact=prod)
        materiali=comp.getComponenti()
        button=self.ButtonImage(materiali,'Componenti',14)
        #button=self.ButtonImage(materiali,'Componenti')
        #button=[]
        #for i in materiali:
        #   c=ProdottiImage.objects.filter(object_id=i['Componenti'], Oggetto ='Button').values('object_id','image')
         #  button.append(c)
        return render(request,'materiali.html',locals())


class ViewsPreventivo(ViewsProd):

    def get(self,request, categoria, prodotto, materiale):
        self.prod=re.sub('-', ' ', prodotto)
        mat=Componente.objects.get(nome__iexact=(re.sub('-',' ',materiale)))
        formati=mat.getFormati()
        campi=self.renderCampi(mat)+self.accessori(mat)
        #accessori=self.accessori(mat)
        giorni=self.getData(mat)
        tabella=self.tabConsegne(mat)
        return render(request,'prodotto.html',locals())
    def renderCampi(self,componente):
        html=''
        campi=componente.campiComponente(True)
        for i in campi:
            html=html+i.campoHtml(componente.nome,'','','',True)
            #if(MappaCampi.objects.filter(figlio=i.id).count()):
              #  pass
               # html=html+i.campoHtml(componente.nome,'','','')
            #else:
                #html=html+i.campoHtml(componente.nome,'','','')
        return html

    def accessori(self,materiale):
        html=''
        accessori=materiale.accessori.all()
        for i in accessori:
            html=html+self.renderCampi(i)
        return html



    def getData(self,materiale):
        list=[]
        a=GiorniFestivi()
        giorni_consegna=GiorniAumento.objects.filter(object_id= materiale).values('nr_gironi_consegna','aumento_percentuale').distinct()
        for i in giorni_consegna:
            x=i['nr_gironi_consegna']
            list.append(x)
        date_consegna=a.CalcoladateFeriali(list)
        for i in giorni_consegna:
            for y in list:
                if y==i['nr_gironi_consegna']:
                    i['data']=date_consegna[y]
                    break
        return giorni_consegna
    def tabConsegne(self,materiale):
        date=GiorniFestivi()
        colonne=[]
        for i in GiorniAumento.objects.filter(object_id= materiale).values('nr_gironi_consegna').distinct():
            colonne.append(i['nr_gironi_consegna'])
        in_righe=GiorniAumento.objects.filter(object_id= materiale).values('quantita').distinct()
        date_consegna=date.CalcoladateFeriali(colonne)
        in_colonna=''
        nr_righe=0
        nr_colonne=0
        riga=''
        for i in date_consegna:
            in_colonna=in_colonna+'<td><div class="col-lg-12 col-md-12 col-sm-12 data"> ' \
                            '<span class="giorno-sett">'+date_consegna[i].strftime('%A')+'</span><br />' \
                            '<span class="giorno" id='+str(nr_colonne)+'>'+date_consegna[i].strftime('%-d')+'</span><br />' \
                            '<span class="mese" id='+str(nr_colonne)+' name='+date_consegna[i].strftime('%m')+'>'+date_consegna[i].strftime('%B')+'</span> </div></td>'
            nr_colonne=nr_colonne+1
        for x in in_righe:
            nr=''
            agg=''
            if(x['quantita']!=0):
                agg='false'
                nr='nr='+str(x['quantita'])
            else:
                agg='true'
            riga=riga+'<tr><td><span class="quantita" agg=%s>%s</span></td>'%(agg,str(x['quantita']))
            for y in colonne:
                cella=GiorniAumento.objects.filter(object_id= materiale,quantita=x['quantita'],nr_gironi_consegna=y).values('quantita','nr_gironi_consegna','aumento_percentuale','sconto_quantita')
                if(cella.count()>0):
                    riga=riga+'<td><label class="checkbox-inline">'\
                            '<input type="radio" class="consegne" name="consegna-materiale" %s id=%s value=%s sc=%s prezzo="0.00" >\
                                <span class="dat_cons">€ 0,00</span>\
                                </label></td>'\
                            %(nr,str(nr_righe),str(cella[0]['aumento_percentuale']),str(cella[0]['sconto_quantita']))
                else:
                    riga=riga+'<td><label class="checkbox-inline"></label></td>'
            riga=riga+'</tr>'
            nr_righe=nr_righe+1
        tabella='<div class="table-responsive text-center">'\
                    '<table class="table">'\
                        '<thead>'\
                            '<tr>' \
                                '<td><img src= "/static/images/icon-consegne.png" alt="consegna" /></td>'\
                                +in_colonna+\
                            '</tr>'\
                        '</thead>'\
                        '<tbody>'\
                            '<div role="group" class="btn-group btn-group-justified">'\
                                +riga+\
                            '</div>'\
                        '</tbody>'\
                    '</table>'\
                '</div>'

        return tabella


    def getName(self,titolo):
        f=True
        name=''
        for i in titolo:
            if(f):
                if(i=='('or i=='{'or i=='['):
                    f=False
                else:
                    if(i!=' '):
                        name=name+i
            else:
                if(i==')'or i=='}'or i==']'):
                    f=True
        return name
    def getFormato(self,formati):
        for i in formati:
           formato=Formati.objects.filter(nome=i['formati']).values('base','altezza')
           i['base']=formato[0]['base']
           i['altezza']=formato[0]['altezza']
        return formati

    def post(self,request):
        componente=request.POST.getlist('componente')[0]
        if 'padre' in request.POST:
            padre=request.POST.getlist('padre')[0]
            valore=request.POST.getlist('valore')[0]
            figli=(request.POST.getlist('figli')[0]).split(';')
            postArray=[]
            self.valoriFiglio(componente,padre,valore,figli,postArray)
            #postArray=self.aggiornaCampi(componente,padre,valore,figlio)
            #for i in figli:
                #postArray.append(self.valoriFiglio(componente,padre,valore,i))
            #return JsonResponse(figli,safe=False)
        else:
            prezzo_a=0
            #componente=request.POST.getlist('componente')[0]
            accessori=[]
            for i in range(int(request.POST.getlist('accessori_nr')[0])):
                accessori.append(request.POST.getlist('accessori['+ str(i) +']')[0])
            for i in accessori:
                dic_a=self.getDictArray(request.POST,i)
                dati_a=self.leggiDati(dic_a,i)
                prezzo_a=prezzo_a+self.prezzo(dati_a)
            dic=self.getDictArray(request.POST,componente)
            dati=self.leggiDati(dic,componente)
            prezzo=self.prezzo(dati)+prezzo_a
            postArray={'prezzo':prezzo}
            #return JsonResponse(request.POST, safe=False)
            #return HttpResponse(componente)
        return JsonResponse(postArray, safe=False)

    def prezzo(self,dati):
        prezzo=Decimal(0)
        data=dati[0]
        spec=dati[1]
        for i in data:
            prezzo=prezzo+i.prezzoVendita*i.calcolo_prezzo.calcolaUm(spec)
        return prezzo




    def valoriFiglio(self,componente,padre,valore,figli,jsData):
        rif=Riferimenti.objects.get(riferimento=componente)
        for i in figli:#
            a=ValoriCampo.objects.get(campo=padre,valori=valore,rif_componente=rif.id)
            mapCamp=MappaCampi.objects.filter(campo=padre,valore_padre=a.id,figlio_id=i)
            b=ValoriCampo.objects.get(campo=mapCamp[0].figlio_id,valori=str(mapCamp[0].valore_figlio),rif_componente=rif.id)
            if(MappaCampi.objects.filter(campo=mapCamp[0].figlio_id,valore_padre=b).count()>0):
                fg=MappaCampi.objects.filter(campo=mapCamp[0].figlio_id,valore_padre=b)
                f=[]
                f.append(fg[0].figlio_id)
                self.valoriFiglio(componente,fg[0].campo_id,str(fg[0].valore_padre),f,jsData)

            jsMap={}
            valD=[]
            for i in mapCamp:
                valD.append(str(i.valore_figlio))
            jsMap['id']=mapCamp[0].figlio_id
            jsMap['non_editabile']=str(mapCamp[0].non_editabile)
            jsMap['valori']=valD
            jsData.append(jsMap)

    def leggiDati(self,dict,componente):
        mat=Componente.objects.get(nome__iexact=componente)
        campi=mat.campiComponente(False)
        rif=[]
        rif_d=[]
        spec={}
        for i in campi:
            if(ValoriCampo.objects.filter(campo_id=i.id,valori_id=dict[str(i.id)],rif_componente_id=Riferimenti.objects.get(riferimento=mat.nome)).count()!=0):
                val=ValoriCampo.objects.get(campo_id=i.id,valori_id=dict[str(i.id)],rif_componente_id=Riferimenti.objects.get(riferimento=mat.nome))
                for x in val.riferimento.all():
                    rif.append(x)
            if(i.specifica_set.count()!=0):
                spec[i.specifica_set.get().id]=dict[str(i.id)]
            if(rif):
                variante=rif[0]
                if(variante.content_object.spec1_id):
                    spec[variante.content_object.spec1_id]=variante.content_object.valore_1
                if(variante.content_object.spec2_id):
                    spec[variante.content_object.spec2_id]=variante.content_object.valore_2
        for i in rif:
            try:
                spec1=i.content_object.spec1_id
                spec2=i.content_object.spec2_id
                if(spec1 is None or spec2 is None):
                    rif_d.append(i.content_object)
                else:
                    if(spec[spec1]==i.content_object.valore_1 and spec[spec2]==i.content_object.valore_2 ):
                        rif_d.append(i.content_object)
            except:
                rif_d.append(i.content_object)
        return rif_d, spec
#####da testare#####
    def getDictArray(self,post,name):
        dic = {}
        for k in post.keys():
            if k.startswith(name):
                rest = k[len(name):]

            # split the string into different components
                parts = [p[:-1] for p in rest.split('[')][1:]
                #id = int(parts[0])
                id = parts[0]
            # add a new dictionary if it doesn't exist yet
                if id not in dic:
                    dic[id] = {}

            # add the information to the dictionary
                dic[id] = post.get(k)
        return dic