from django import forms
from django.forms import ModelForm
from anagrafiche.models import *
from django.utils.safestring import mark_safe
from django.forms.widgets import RadioFieldRenderer
from django.utils.encoding import force_unicode
from django.contrib.auth.models import User
import datetime
from django.contrib.auth.hashers import PBKDF2PasswordHasher
#class clientForm(ModelForm):
 #   class Meta:
  #      model=cliente

class HorizRadioRenderer(RadioFieldRenderer):
    """ this overrides widget method to put radio buttons horizontally
        instead of vertically.
    """
    def render(self):
            """Outputs radios"""
            return  mark_safe(u'%s' % u'\n'.join([u'%s'  % force_unicode(w) for w in self]))

class registrazioneForm(forms.Form):
    CONTINENTE_CHOICES=[('','--scegli un continente--')]+[(c.continente,c.continente) for c in continente.objects.all()]
    PAESE_CHOICES=[('', '-- scegli un continente prima --')]
    TIPO_CLIENTE =[('','---'),('Associazione','Associazione'),('Ditta','Ditta individuale - Libero Professionista'),('Privato','Privato'),('Societa','Societa')]
    PREFISSO=[('','---')]
    ACC=[('True','Accetto'),('False','Non Accetto')]
    #continente=forms.ChoiceField(choices=CONTINENTE_CHOICES,widget=forms.Select(attrs={'class':'btn btn-default  col-lg-3 col-md-3 col-sm-3','onchange':'get_continente_paese()'}))
    #paese=forms.ChoiceField(choices=PAESE_CHOICES,widget=forms.Select(attrs={'class':'btn btn-default  col-lg-3 col-md-3 col-sm-3 col-lg-offset-1 col-md-offset-1 col-sm-offset-1'}))
    #tipo_cliente=forms.ChoiceField(choices=TIPO_CLIENTE,initial={''},widget=forms.Select(attrs={'class':'btn btn-default  col-lg-3 col-md-3 col-sm-3 col-lg-offset-1 col-md-offset-1 col-sm-offset-1','onchange':'get_tipo()'}))
    persona_riferimento=forms.CharField(max_length=20,widget=forms.TextInput)
    prefisso_int=forms.ChoiceField(required=False,choices=PREFISSO,widget=forms.Select(attrs=({'class':'btn btn-default  col-lg-0 col-md-1 col-sm-1 col-lg-offset-1 col-md-offset-0 col-sm-offset-0'})))
    telefono=forms.CharField(widget=forms.TextInput())
    cellulare=forms.CharField(required=False,widget=forms.TextInput())
    fax=forms.CharField(required=False,widget=forms.TextInput())
    email=forms.CharField(widget=forms.TextInput())
    ripeti_email=forms.CharField(widget=forms.TextInput())
    username=forms.CharField(widget=forms.TextInput())
    password=forms.CharField(widget=forms.PasswordInput())
    ripeti_password=forms.CharField(widget=forms.PasswordInput())
    privacy=forms.BooleanField()
    newsletter=forms.BooleanField(required=False)
    ###Azienda
    def __init__(self,cont,*args, **kwargs):
        super(registrazioneForm,self).__init__(*args, **kwargs)
        PAESE_CHOICES=[(c.sigla_paese,c.paese) for c in paese.objects.filter(continente = cont).all()]
        TIPO_CLIENTE =[('','---'),('Associazione','Associazione'),('Ditta','Ditta individuale - Libero Professionista'),('Privato','Privato'),('Societa','Societa')]
        self.fields['tipo_cliente']=forms.ChoiceField(choices=TIPO_CLIENTE,initial={''},widget=forms.Select(attrs={'class':'btn btn-default  col-lg-3 col-md-3 col-sm-3 col-lg-offset-1 col-md-offset-1 col-sm-offset-1'}))
        self.fields['paese']=forms.ChoiceField(choices=PAESE_CHOICES,widget=forms.Select(attrs={'class':'btn btn-default  col-lg-3 col-md-3 col-sm-3 col-lg-offset-1 col-md-offset-1 col-sm-offset-1'}))
        self.fields['continente']=forms.ChoiceField(initial=cont, choices=self.CONTINENTE_CHOICES,widget=forms.Select(attrs={'class':'btn btn-default  col-lg-3 col-md-3 col-sm-3'}))
    def save(self,form):
        data=self.cleaned_data
        ft=form.cleaned()
        if(data['tipo_cliente']=="Privato" or "Ditta"):
            user=User(username=data['username'],email=data['email'],first_name=ft['nome'],last_name=ft['cognome'])
            user.set_password(data['password'])
        else:
            user=User(username=data['username'],password=data['password'],email=data['email'])
        user.save()
        cli=cliente(user=user,denominazione=ft['denominazione'],societa=ft['tipo'],p_iva=ft['partita_iva'],cod_fiscale=ft['codice_fiscale'],
                    telefono=data['telefono'],cellulare=data['cellulare'],fax=data['fax'],tipo=data['tipo_cliente'],privacy='true',
                    newsletter=data['newsletter'],data_inscrizione=datetime.datetime.now())
        ind=indirizzo(indirizzo=ft['indirizzo'],citta=ft['localita'],cap=ft['cap'],provincia=ft['provincia'],nazione=data['paese'])
        ind.save()
        cli.save()
        col=indirizzo_mycontact(riferimento='Sede Principale',indirizzo=ind,contact=cli,tipo='FT')
        rif=rubrica(nome=data['persona_riferimento'])
        rif.save()
        ref=referente(referente=rif,azienda=cli)
        ref.save()
        col.save()

class fatturazioneForm(forms.Form):
    cognome=forms.CharField(required=False,widget=forms.TextInput())
    nome=forms.CharField(required=False,widget=forms.TextInput())
    denominazione=forms.CharField(required=False,max_length=20,widget=forms.TextInput())
    #tipo=forms.ChoiceField(choices=TIPO_SOCIETA,widget=forms.Select(attrs={'class':'btn btn-default  col-lg-3 col-md-3 col-sm-3 col-lg-offset-1 col-md-offset-1 col-sm-offset-1'}))
    #provincia=forms.ChoiceField(required=False,choices=PROVINCIA,widget=forms.Select())
    partita_iva=forms.CharField(required=False,widget=forms.TextInput())
    codice_fiscale=forms.CharField(widget=forms.TextInput(attrs={'class':'uppercase'}))
    localita=forms.CharField(widget=forms.TextInput())
    indirizzo=forms.CharField(widget=forms.TextInput())
    cap=forms.CharField(widget=forms.TextInput())

    def __init__(self,paese,*args, **kwargs):
        super(fatturazioneForm,self).__init__(*args, **kwargs)
        PROVINCIE=[(c.sigla_provincia,c.provincia) for c in provincia.objects.filter(stato_appartenenza=paese).all()]
        TIPI_SOCIETA=[(d.sigla_societa,d.sigla_societa)for d in tipo_societa.objects.filter(paese_riferimento = paese).all()]
        if(PROVINCIE):
            self.fields['provincia']=forms.ChoiceField(required=False,choices=PROVINCIE,widget=forms.Select())
        if(TIPI_SOCIETA):
            self.fields['tipo']=forms.ChoiceField(required=False,choices=TIPI_SOCIETA,widget=forms.Select)
    def cleaned(self):
        data=self.cleaned_data
        return data

