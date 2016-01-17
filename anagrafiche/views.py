from django.shortcuts import render
from django.db import models
from django.template import Context, loader
from django.http import HttpResponse, Http404
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import Context,RequestContext
from anagrafiche.models import *
from anagrafiche.forms import *
from django import template
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth.models import User




class registrazione(View):
    c={}
    tipo_cliente={}
    def get(self, request):
        if request.is_ajax():
            if 'continente' in request.GET:
                self.continente=request.GET.get('continente', '')
                form=registrazioneForm(self.continente, auto_id='%s')
                form_ft=fatturazioneForm('', auto_id='%s')
                paesi_dict={}
                paesi= paese.objects.filter(continente = self.continente).all()
                for Paese in paesi:
                    paesi_dict[Paese.sigla_paese] = Paese.paese
                #return render_to_response ('paese_request.html',locals())
                return JsonResponse(paesi_dict)
            elif 'tipo_cliente' in request.GET:
                self.tipo_cliente=request.GET.get('tipo_cliente', '')
                tipo=self.tipo_cliente
                p=request.GET.get('paese', '')
                form=fatturazioneForm( p ,auto_id='%s')
                #form_ft=form.selectOption(registrazione.paese)
                return render_to_response('tipo.html',locals() )
            elif 'username' in request.GET:
                us=User.objects.filter(username=request.GET.get('username',''))
                if(us.count()):
                    return HttpResponse("true")
                else:
                    return HttpResponse("false")
            elif 'email' in request.GET:
                us=User.objects.filter(email=request.GET.get('email',''))
                if(us.count()):
                    return HttpResponse("true")
                else:
                    return HttpResponse("false")
            elif 'partita_iva' in request.GET:
                cli=cliente.objects.filter(p_iva=request.GET.get('partita_iva',''))
                if(cli.count()):
                    return HttpResponse("true")
                else:
                    return HttpResponse("false")
            elif 'codice_fiscale' in request.GET:
                cli=cliente.objects.filter(cod_fiscale=request.GET.get('codice_fiscale',''))
                if(cli.count()):
                    return HttpResponse("true")
                else:
                    return HttpResponse("false")
        else:
            self.c.update(csrf(request))
            form=registrazioneForm('Europa', auto_id='%s')
            return render(request,'registrazione.html',locals())

    def post(self, request):
        con=request.POST['continente']
        pae=request.POST['paese']
        form_re=registrazioneForm(con,request.POST)
        form_ft=fatturazioneForm(pae,request.POST)
        if form_re.is_valid() and form_ft.is_valid():
            form_re.save(form_ft)
            return HttpResponseRedirect('/')
        else:
            msg=form_re.errors
            msg1=form_ft.errors
            return render(request,'registrazione.html',locals())

    #def ricaricaPagina(self,request):
        #form=registrazioneForm(self.continente, auto_id='%s')
        #return HttpResponseRedirect('registrazione.html',locals())

