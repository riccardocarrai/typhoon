from django.db import models
from anagrafiche.models import macchina
from catalogo.media import *
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from decimal import *

# Create your models here.


class UM(models.Model):
    UM=models.CharField(max_length=2,primary_key=True)
    descrizione=models.CharField(max_length=30,blank=True)
    def __unicode__(self):
        return self.UM
    class Meta:
        verbose_name_plural="Unita di Misura"

class ProdottiImage(models.Model):
    image=models.ImageField(upload_to="ImmaginiProdotto")
    content_type=models.ForeignKey(ContentType,blank=True)
    object_id = models.CharField(max_length=30,blank=True)
    content_object = GenericForeignKey("content_type", "object_id")
    Oggetto=models.ForeignKey(TipoOggetto)
    altezza=models.IntegerField()
    larghezza=models.IntegerField()
    def save(self, *args, **kwargs):
        if(ProdottiImage.objects.filter(object_id=self.object_id).count()==0 and self.Oggetto==TipoOggetto.objects.get(oggetto='Button')):
            rif=Riferimenti.objects.get(object_id=self.object_id)
            img=ImmaginiCampo(image=self.image,valori=Valori.objects.get(valore=rif.riferimento))
            img.save()
        super(ProdottiImage,self).save(*args, **kwargs)
            #rif=Riferimenti(riferimento=str(self.nome),content_object=self)
            #val=Valori(valore=str(self.nome))
            #rif.save()
            #val.save()
    def delete(self, *args, **kwargs):

        super(ProdottiImage,self).delete(*args, **kwargs)
    def __unicode__(self):
        return u"%s" % (self.image)

class Specifica(models.Model):
    specifica=models.CharField(max_length=30)
    UM=models.ForeignKey(UM)
    campo=models.ManyToManyField(Campo)
    def __unicode__(self):
        return u"%s" " " u"%s" % (self.specifica,self.UM)
    class Meta:
        verbose_name_plural = "Specifiche"

class Formati(models.Model):

    nome=models.CharField(max_length=40)
    spec1=models.ForeignKey(Specifica,related_name='Specifica1',verbose_name='Specifica',blank=True,null=True)
    valore_1=models.IntegerField(blank=True,null=True,verbose_name='')
    spec2=models.ForeignKey(Specifica,related_name='Specifica2',verbose_name='Specifica',blank=True,null=True)
    valore_2=models.IntegerField(blank=True,null=True,verbose_name='')
    def save(self, *args, **kwargs):
       if(Formati.objects.filter(nome=self.nome).count()==0):
            super(Formati,self).save(*args, **kwargs)
            rif=Riferimenti(riferimento=str(self.nome),content_object=self)
            val=Valori(valore=str(self.nome))
            rif.save()
            val.save()
    def __unicode__(self):
        return u"%s" % (self.nome)
    class Meta:
        verbose_name_plural = "Formati"






class calcoloUm(models.Model):
    nome=models.CharField(max_length=30,primary_key=True)
    descrizione=models.CharField(max_length=30,blank=True)
    specifica=models.ManyToManyField(Specifica,through='conversione')

    def specifiche(self):
        camp=[]
        campi=self.specifica.all()
        for i in campi:
            camp.append(i.id)
        return camp
    def calcolaUm(self,dati):
        getcontext().prec=4
        spec=self.specifica.all()
        if(self.nome=='MQ'):
            mq=Decimal(1)
            conv=Decimal(1)
            x=0
            for i in spec:
                v=Decimal(dati [i.id])
                mq=mq*v
                conv=conv*i.conversione_set.get(um=self.nome).fatt_conversione
            mq=mq/conv
            if(mq<1):
                mq=Decimal(1)
            elif(mq%Decimal(0.5)>0):
                r=mq%Decimal(1)
                if(r<0.5):
                     q=Decimal(0.5)-r
                else:
                     q=Decimal(1)-r
                mq=mq+q
        elif(self.nome=='PZ'):
            for i in spec:
                mq=Decimal(dati [i.id])
        else:
            mq=Decimal(0)
        return mq

    def __unicode__(self):
        return u"%s" % (self.nome)
    class Meta:
        verbose_name_plural = "Calcolo Unita di misura"

class variante(models.Model):
    nome = models.CharField(max_length=30,primary_key=True)
    costo=models.DecimalField(max_digits=6,decimal_places=2)
    UM=models.ForeignKey(UM)
    def __unicode__(self):
        return u"%s" % (self.nome)
    def save(self, *args, **kwargs):
        if(variante.objects.filter(nome=self.nome).count()==0):
            super(variante,self).save(*args, **kwargs)
            rif=Riferimenti(riferimento=str(self.nome),content_object=self)
            val=Valori(valore=str(self.nome))
            rif.save()
            val.save()
    def delete(self,*args,**kwargs):
        rif=Riferimenti.objects.get(object_id=self.nome,content_type=ContentType.objects.get_for_model(self))
        rif.delete()
        super(variante,self).delete(*args, **kwargs)
    class Meta:
        verbose_name_plural = "Varianti"


class Lavorazione(models.Model):
    nome = models.CharField(max_length=50,primary_key=True)
    costo=models.DecimalField(max_digits=6,decimal_places=2)
    UM=models.ForeignKey(UM)
    macchina=models.ForeignKey(macchina,blank=True)
    addetti=models.IntegerField(blank=True)

    def save(self, *args, **kwargs):
        if(Lavorazione.objects.filter(nome=self.nome).count()==0):
            super(Lavorazione,self).save(*args, **kwargs)
            rif=Riferimenti(riferimento=str(self.nome),content_object=self)
            rif.save()


    class Meta:
        verbose_name_plural = "Lavorazioni"
    def __unicode__(self):
        return self.nome




class Componente (models.Model):
    nome = models.CharField(max_length=40,primary_key=True)
    descrizione=models.TextField()
    varianti = models.ManyToManyField(variante, through='VarianteComponente',blank=True)
    lavorazioni=models.ManyToManyField(Lavorazione, through='LavorazioneComponente',blank=True)
    formati=models.ManyToManyField(Formati,through='ScontoFormato',blank=True)
    accessori=models.ManyToManyField('self',through='Accessori',symmetrical=False,related_name='acessori',blank=True)
    Campi=models.ManyToManyField(Campo,through='CampiComponente')
    def lavorazioniObb(self):
        a=self.lavorazionecomponente_set.all()
        lav=[]
        for i in a:
            if(i.tipoLavorazione=='O'):
               lav.append(i)
        return lav
    def prezzoVariante(self,variante):
        var=self.variantecomponente_set.get(variante=variante)
        prezzo=var.prezzoVendita
        um=var.calcolo_prezzo
        return prezzo, um

    def lavorazioniAgg(self):
        a=self.lavorazionecomponente_set.all()
        lav=[]
        for i in a:
            if(i.tipoLavorazione=='A' and not i.materiale):
            #if(i.tipoLavorazione=='A'):
               lav.append(i)
        return lav

    def save(self, *args, **kwargs):
        super(Componente,self).save(*args, **kwargs)
        if((Riferimenti.objects.filter(object_id=self.nome).count())==0 ):
            rif=Riferimenti(riferimento=str(self.nome),content_object=self)
            rif.save()
    def getAccessori(self):
        return self.accessori.all()

    def getVarianti(self):
        return self.varianti.all()
    def getFormati(self):
        return self.formati.all()

    def campiComponente(self,re_type):
        campi=[]
        c_camp=self.campicomponente_set.all().order_by('ordine_visualizzazione')
        for i in c_camp:
            if(re_type and i.figli):
                pass
            else:
                campi.append(i.campo)
        return campi

    def __unicode__(self):
        return self.nome
    class Meta:
        verbose_name_plural = "Componenti"



class Prodotto(models.Model):
    prodotto=models.CharField(max_length=40, primary_key=True)
    descrizione = models.TextField(blank=True)
    short_description=models.TextField(blank=True)
    sconto_globale=models.PositiveSmallIntegerField(default='0')
    prodotto_new=models.BooleanField(default=False)
    in_evidenza = models.BooleanField(default=False)
    Componenti=models.ManyToManyField(Componente,blank=True)

    class Meta:
        verbose_name_plural = "Prodotti"
    def __unicode__(self):
        return self.prodotto
    def getComponenti(self):
        return self.Componenti.all()

class ScontoFormato(models.Model):
    componente=models.ForeignKey(Componente)
    formato=models.ForeignKey(Formati)
    sconto=models.IntegerField()
    campo=models.ForeignKey(Campo,blank=True,null=True)
    default=models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        if(Valori.objects.filter(valore=self.formato).count()==0):
            val=Valori(valore=self.formato)
            val.save()
        else:
            val=Valori.objects.get(valore=self.formato)
        super(ScontoFormato,self).save(*args, **kwargs)
        if(CampiComponente.objects.filter(campo=self.campo,componente=self.componente).count()==0):
                    c=CampiComponente(componente=self.componente,campo=self.campo,ordine_visualizzazione=self.componente.campicomponente_set.count()+1)
                    c.save()
        img=Immagini.objects.filter(object_id=self.formato.id,content_type=ContentType.objects.get_for_model(self.formato), Oggetto='Button')
        rif=Riferimenti.objects.get(riferimento=str(self.formato.nome))
        map=ValoriCampo.objects.get_or_create(campo=self.campo, rif_componente=Riferimenti.objects.get(riferimento=str(self.componente.nome)),valori_id=val)
        if(img.count()!=0):
            imgC=img.get()
            map[0].immagine=imgC
        map[0].save()
        map[0].riferimento.add(rif)
    def delete(self,*args,**kwargs):
        rif=Riferimenti.objects.get(riferimento=str(self.formato.nome),object_id=self.formato.id,content_type=ContentType.objects.get_for_model(self.formato))
        val=rif.valoricampo_set.get()
        rif_c=val.riferimento.count()
        if(rif_c==1):
            val.delete()
        super(ScontoFormato,self).delete(*args, **kwargs)

class VarianteComponente(models.Model):
    variante=models.ForeignKey(variante)
    componente=models.ForeignKey(Componente)
    prezzoVendita=models.DecimalField(max_digits=6,decimal_places=2)
    calcolo_prezzo=models.ForeignKey(calcoloUm)
    spec1=models.ForeignKey(Specifica,related_name='Prima_Specifica',verbose_name='Specifica',blank=True,null=True)
    valore_1=models.IntegerField(blank=True,null=True,verbose_name='')
    spec2=models.ForeignKey(Specifica,related_name='Seconda_Specifica',verbose_name='Specifica',blank=True,null=True)
    valore_2=models.IntegerField(blank=True,null=True,verbose_name='')
    campo=models.ForeignKey(Campo)
    valore_campo=models.CharField(max_length=40,null=True,blank=True)
    default=models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        if(self.valore_campo==''):
            self.valore_campo=str(self.variante.nome)
        if(Valori.objects.filter(valore=self.valore_campo).count()==0):
            val=Valori(valore=self.valore_campo)
            val.save()
        else:
            val=Valori.objects.get(valore=self.valore_campo)
        super(VarianteComponente,self).save(*args, **kwargs)
        if(CampiComponente.objects.filter(campo=self.campo,componente=self.componente).count()==0):
            c=CampiComponente(componente=self.componente,campo=self.campo,ordine_visualizzazione=self.componente.campicomponente_set.count()+1)
            c.save()
        img=Immagini.objects.filter(object_id=self.variante.nome,content_type=ContentType.objects.get_for_model(self.variante), Oggetto='Button')
        rif=Riferimenti.objects.filter(riferimento=str(self.variante)+' - '+str(self.componente),object_id=self.id,content_type=ContentType.objects.get_for_model(self))
        if(rif.count()==0):
            rif=Riferimenti(riferimento=str(self.variante)+' - '+str(self.componente),content_object=self)
            rif.save()
            rifC=True
        else:
            rifC=False
        map=ValoriCampo.objects.filter(campo=self.campo, rif_componente=Riferimenti.objects.get(riferimento=str(self.componente.nome)),valori_id=val)
        if(map.count()==0):
            if(img.count()!=0):
                map=ValoriCampo(campo=self.campo, rif_componente=Riferimenti.objects.get(riferimento=str(self.componente.nome)),immagine=img.get(),valori_id=val)
            else:
                map=ValoriCampo(campo=self.campo, rif_componente=Riferimenti.objects.get(riferimento=str(self.componente.nome)),valori_id=val)
            map.save()
        else:
            map=ValoriCampo.objects.get(campo=self.campo, rif_componente=Riferimenti.objects.get(riferimento=str(self.componente.nome)),valori_id=val)

        if(rifC):
            map.riferimento.add(rif)


    def delete(self,*args,**kwargs):
        rif=Riferimenti.objects.get(riferimento=str(self.variante)+' - '+str(self.componente),object_id=self.id,content_type=ContentType.objects.get_for_model(self))
        val=rif.valoricampo_set.get()
        rif_c=val.riferimento.count()
        if(rif_c==1):
            val.delete()
        rif.delete()
        super(VarianteComponente,self).delete(*args, **kwargs)
    def __unicode__(self):
        return u"%s-" u"%s" u"%sx" u"%s" % (self.variante,self.componente,self.valore_1,self.valore_2)
    class Meta:
        verbose_name_plural = "Varianti"


class LavorazioneComponente(models.Model):
    lavorazione=models.ForeignKey(Lavorazione)
    componente=models.ForeignKey(Componente)
    tipoLavorazione=models.CharField(max_length=1,choices=(('O','Obbligatoria'),('A','Aggiuntiva')))
    prezzoVendita=models.DecimalField(max_digits=6,decimal_places=2)
    calcolo_prezzo=models.ForeignKey(calcoloUm)
    spec1=models.ForeignKey(Specifica,related_name='Specifica_1',verbose_name='Specifica',blank=True,null=True)
    valore_1=models.IntegerField(blank=True,null=True,verbose_name='')
    spec2=models.ForeignKey(Specifica,related_name='Specifica_2',verbose_name='Specifica',blank=True,null=True)
    valore_2=models.IntegerField(blank=True,null=True,verbose_name='')
    campo=models.ForeignKey(Campo,null=True,blank=True)
    valore_campo=models.CharField(max_length=40,null=True,blank=True)
    def lavorazionePrezzo(self):
        return self.prezzoVendita ,self.calcolo_prezzo
    def CampiLav(self):
        if(self.tipoLavorazione=='A'):
            #dati=[]
            map={}
            c=Riferimenti.objects.get(object_id=self)
            campi=c.valoricampo_set.all()
            map['lavorazione']=self.lavorazione.nome
            map['valore']=campi.get().valori.valore
            map['campo']=campi.get().campo_id
            map['valoreId']=campi.get().id
            map['titolo']=campi.get().campo.titolo
            #dati.append(map)
            return map

    def save(self, *args, **kwargs):
        if(self.tipoLavorazione=='A'):
            if(self.valore_campo==''):
                self.valore_campo=str(self.lavorazione.nome)
            if(Valori.objects.filter(valore=self.valore_campo).count()==0):
                val=Valori(valore=self.valore_campo)
                val.save()
            else:
                val=Valori.objects.get(valore=self.valore_campo)
            super(LavorazioneComponente,self).save(*args, **kwargs)
            if(CampiComponente.objects.filter(campo=self.campo,componente=self.componente).count()==0):
                    c=CampiComponente(componente=self.componente,campo=self.campo,ordine_visualizzazione=self.componente.campicomponente_set.count()+1)
                    c.save()
            rif=Riferimenti.objects.filter(riferimento=str(self.lavorazione)+' - '+str(self.componente),object_id=self.id,content_type=ContentType.objects.get_for_model(self))
            if(rif.count()==0):
                rif=Riferimenti(riferimento=str(self.lavorazione)+' - '+str(self.componente),content_object=self)
                rif.save()
                rifC=True
            else:
                rifC=False
            map=ValoriCampo.objects.filter(campo=self.campo, rif_componente=Riferimenti.objects.get(riferimento=str(self.componente.nome)),valori_id=val)
            if(map.count()==0):
                map=ValoriCampo(campo=self.campo, rif_componente=Riferimenti.objects.get(riferimento=str(self.componente.nome)),valori_id=val)
                map.save()
            else:
                map=map.get()
            if(rifC):
                map.riferimento.add(rif)
        else:
            super(LavorazioneComponente,self).save(*args, **kwargs)
    def delete(self,*args,**kwargs):
        rif=Riferimenti.objects.get(riferimento=str(self.lavorazione)+' - '+str(self.componente),object_id=self.id,content_type=ContentType.objects.get_for_model(self))
        val=rif.valoricampo_set.get()
        val.delete()
        rif.delete()
        super(LavorazioneComponente,self).delete(*args, **kwargs)

    def __unicode__(self):
        return u"%s" % (self.lavorazione)
    class Meta:
        verbose_name_plural = "Tipo Lavorazione"



class Accessori(models.Model):
    from_componente=models.ForeignKey(Componente,related_name='componente')
    to_componente=models.ForeignKey(Componente,related_name='accessorio')


class GiorniAumento(models.Model):
    content_type=models.ForeignKey(ContentType,blank=True)
    object_id = models.CharField(max_length=30,blank=True)
    content_object = GenericForeignKey("content_type", "object_id")
    nr_gironi_consegna=models.IntegerField()
    quantita=models.IntegerField()
    sconto_quantita=models.DecimalField(max_digits=4,decimal_places=2)
    aumento_percentuale=models.DecimalField(max_digits=4,decimal_places=2)

class CampiComponente(models.Model):
    componente=models.ForeignKey(Componente)
    campo=models.ForeignKey(Campo)
    ordine_visualizzazione=models.IntegerField(null=True,blank=True)
    padri=models.BooleanField(default=False)
    figli=models.BooleanField(default=False)

class conversione(models.Model):
    um=models.ForeignKey(calcoloUm)
    specifica=models.ForeignKey(Specifica)
    fatt_conversione=models.DecimalField(max_digits=6,decimal_places=2)

class caratteristica(models.Model):
    specifica=models.ForeignKey(Specifica)
    valore=models.CharField(max_length=30)
    content_type=models.ForeignKey(ContentType,blank=True)
    object_id = models.CharField(max_length=30,blank=True)
    content_object = GenericForeignKey("content_type", "object_id")


