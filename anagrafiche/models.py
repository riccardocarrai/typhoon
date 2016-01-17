import datetime
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User

# from prodotti.models import Componente
# Create your models here.


class GiorniFestivi(models.Model):
    giorno=models.CharField(max_length=2)
    mese=models.CharField(max_length=2,choices=(('1','Gennaio'),('2','Febbraio'),('3','Marzo'),('4','Aprile'),
                                                ('5','Maggio'),('6','Giugno'),('7','Luglio'),('8','Agosto'),
                                                ('9','Settembre'),('10','Ottobre'),('11','Novembre'),('12','Dicembre')))
    festivita=models.CharField(max_length=30)

    def CalcoladateFeriali(self,day_list=[]):
        now=datetime.datetime.now()
        list={}
        festivita=0
        for i in day_list:
            if(now.hour>=13):
                x=i+festivita+1
            else:
                x=i+festivita
            delta=datetime.timedelta(x)
            delta_date=now+delta
            while True:
                if(delta_date.strftime("%w")=='6'or delta_date.strftime("%w")=='0'
                   or GiorniFestivi.objects.filter(giorno=delta_date.day,mese=delta_date.month).count()
                    or delta_date.date()==(self.CalcolaPasqua(now.year)).date()):
                    x=x+1
                    festivita=festivita+1
                    a=datetime.timedelta(x)
                    delta_date=now+a
                else:
                    break
            list[i]=delta_date.date()
        return list
    def CalcolaData(self,day):
        day_n=day
        now=datetime.datetime.now()
        if(now.hour>=13):
            day_n=day+1
        while True:
            delta=datetime.timedelta(day_n)
            delta_date=now+delta
            if(delta_date.strftime("%w")=='6'or delta_date.strftime("%w")=='0'
                or GiorniFestivi.objects.filter(giorno=delta_date.day,mese=delta_date.month).count()
                or delta_date.date()==(self.CalcolaPasqua(now.year)).date()):
                    day_n=day_n+1
                    #delta_date=now+datetime.timedelta(day)
                    #festivita=festivita+1
            else:
                delta_date=now+datetime.timedelta(day+day_n)
                return delta_date.date()

    def CalcolaPasqua(self,anno):
        a=anno%19
        b=anno%4
        c=anno%7
        d=(19*a+24)%30
        e=(2*b+4*c+6*d+5)%7
        f=d+e
        if(f<10):
            giorno_pasqua=f+22
            mese_pasqua=3
        else:
            giorno_pasqua=f-9
            mese_pasqua=4
        pasqua=datetime.datetime(anno,mese_pasqua,giorno_pasqua)
        delta=datetime.timedelta(1)
        pasquetta=pasqua+delta
        return pasquetta










class CalendarioFestivita(models.Model):
    pass

class continente(models.Model):
    continente=models.CharField(max_length=40,primary_key=True)
    def __unicode__(self):
        return self.continente

    class Meta:
        verbose_name_plural = "Continenti"

class paese(models.Model):
    sigla_paese=models.CharField(max_length=3,primary_key=True)
    paese=models.CharField(max_length=40)
    continente=models.ForeignKey(continente)
    prefisso_internazionale=models.CharField(max_length=5)
    def __unicode__(self):
        return self.paese
    class Meta:
        verbose_name_plural = "Paesi"

class cap(models.Model):
    cap=models.CharField(max_length=5,primary_key=True)


class provincia(models.Model):
    sigla_provincia=models.CharField(max_length=5,primary_key=True)
    provincia=models.CharField(max_length=100)
    stato_appartenenza=models.ForeignKey(paese)
    def __unicode__(self):
        return self.provincia
    class Meta:
        verbose_name_plural = "Provincie"

class localita(models.Model):
    comune=models.CharField(max_length=50,primary_key=True)
    provincia=models.ForeignKey(provincia)
    cap=models.ManyToManyField(cap)


class tipo_societa(models.Model):
    sigla_societa=models.CharField(max_length=5,primary_key=True)
    descrizione=models.CharField(max_length=50)
    paese_riferimento=models.ForeignKey(paese)
    def __unicode__(self):
        return self.sigla_societa
    class Meta:
        verbose_name_plural = "Tipo societa"



class indirizzo(models.Model):
    indirizzo = models.CharField(max_length=150)
    citta = models.CharField(max_length=100)
    cap = models.IntegerField()
    provincia = models.CharField(max_length=2)
    nazione = models.CharField(max_length=3)
    def __unicode__(self):
        return self.indirizzo


class campo_rubrica(models.Model):
    campo=models.CharField(max_length=50,primary_key=True)


class rubrica(models.Model):
    nome = models.CharField(max_length=40)
    campi = models.ManyToManyField(campo_rubrica,through="voce_rubrica",blank=True)
    class Meta:
        verbose_name_plural = "Rubrica"
    def __unicode__(self):
        return self.nome

class voce_rubrica(models.Model):
    campo = models.ForeignKey(campo_rubrica)
    rubrica = models.ForeignKey(rubrica)
    dato = models.CharField(max_length=30)



class MyContact(models.Model):
    denominazione = models.CharField(max_length=150,blank=True)
    societa=models.CharField(max_length=10,blank=True)
    p_iva = models.CharField(max_length=13, blank=True)
    cod_fiscale = models.CharField(max_length=20)
    telefono = models.CharField(max_length=25,blank=True)
    cellulare = models.CharField(max_length=25, blank=True)
    fax = models.CharField(max_length=25, blank=True)
    indirizzi = models.ManyToManyField(indirizzo, through='indirizzo_mycontact', blank=True)
    #indirizzi = models.ManyToManyField(indirizzo, related_name="%(app_label)s_%(class)s_related", blank=True)
    tipo = models.CharField(max_length=150)
    #dipendenti = models.ManyToManyField(rubrica, related_name="%(app_label)s_%(class)s_related", blank=True)
    dipendenti = models.ManyToManyField(rubrica, through='referente', blank=True)
    privacy=models.BooleanField(verbose_name="Accettazione privacy",default=False)
    newsletter=models.BooleanField(verbose_name="Iscrizione Newsletter", blank=True,default=False)
    data_inscrizione=models.DateTimeField(verbose_name="Iscrizione accettazione Condizioni")




class cliente(MyContact):
    user = models.OneToOneField(User, blank=True)
    class Meta:
        verbose_name_plural = "Clienti"


class contatto(MyContact):
    nome = models.CharField(max_length=10)
    cognome = models.CharField(max_length=10)
    email=models.EmailField()
    class Meta:
        verbose_name_plural = "Contatti"


class impiegati(models.Model):
    user = models.OneToOneField(User)
    ruolo = models.CharField(max_length=20)
    costo_orario = models.DecimalField(max_digits=4, decimal_places=2)
    rubrica = models.ManyToManyField(rubrica)

    class Meta:
        verbose_name_plural = "Impiegati"


class macchina(models.Model):
    nome = models.CharField(max_length=50)
    funzione = models.CharField(max_length=1, choices=(('S', 'Stampa'), ('T', 'Taglio'), ('F', 'Finisaggio')))

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Macchine"


class referente(models.Model):
    referente=models.ForeignKey(rubrica)
    azienda=models.ForeignKey(MyContact)
    funzione=models.CharField(max_length=10)

class indirizzo_mycontact(models.Model):
    riferimento=models.CharField(max_length=30)
    indirizzo = models.ForeignKey(indirizzo)
    contact=models.ForeignKey(MyContact)
    tipo = models.CharField(max_length=2, choices=(('FT', 'Fatturazione'), ('SP', 'Spedizione')))
    class Meta:
        verbose_name_plural = "Indirizzi"



