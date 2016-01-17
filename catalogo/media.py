from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from re import *
import re
class TipoOggetto(models.Model):
    oggetto=models.CharField(max_length=20,primary_key=True)
    def __unicode__(self):
        return self.oggetto
    class Meta:
        verbose_name_plural='Oggetti'

class media(models.Model):
    titolo=models.CharField(max_length=20)
    image=models.ImageField()
    didascalia=models.TextField()
    pagina=models.CharField(max_length=20)
    url=models.URLField(blank=True)
    tipo=models.CharField(max_length=2,choices=(('1','Slider'),('2','Adv')))
    def __unicode__(self):
        return self.titolo

class Immagini(models.Model):
    titolo=models.CharField(max_length=40)
    image=models.ImageField(upload_to="Immagini")
    content_type=models.ForeignKey(ContentType,null=True,blank=True)
    object_id = models.CharField(max_length=40,null=True,blank=True)
    content_object = GenericForeignKey("content_type", "object_id")
    Oggetto=models.ForeignKey(TipoOggetto)
    altezza=models.IntegerField()
    larghezza=models.IntegerField()
    thumbnail = models.ImageField(upload_to="thumbnails/", editable=False,null=True,blank=True)

    def save(self):
        super(Immagini, self).save()
        if(Riferimenti.objects.filter(object_id=self.object_id,content_type=self.content_type).count()!=0):
            rif=Riferimenti.objects.get(object_id=self.object_id,content_type=self.content_type)
            if(rif.valoricampo_set.count()!=0):
                val=rif.valoricampo_set.get()
                val.immagine=self
                val.save()
    #url=models.URLField(blank=True)
    #def save(self):
        #for field in self._meta.fields:
            #if field.name == 'image':
                #field.upload_to = 'Prodotto/%s' % self.titolo
        #super(Image, self).save()
    #def save(self):
     #   import os
      #  from PIL import Image
       # from cStringIO import StringIO
        #from django.core.files.uploadedfile import SimpleUploadedFile

        # Set our max thumbnail size in a tuple (max width, max height)
        #THUMBNAIL_SIZE = (50, 50)

        # Open original photo which we want to thumbnail using PIL's Image
        # object
        #image = Image.open(self.photo.name)

        # Convert to RGB if necessary
        # Thanks to Limodou on DjangoSnippets.org
        # http://www.djangosnippets.org/snippets/20/
        #if image.mode not in ('L', 'RGB'):
         #   image = image.convert('RGB')

        # We use our PIL Image object to create the thumbnail, which already
        # has a thumbnail() convenience method that contrains proportions.
        # Additionally, we use Image.ANTIALIAS to make the image look better.
        # Without antialiasing the image pattern artifacts may result.
        #image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

        # Save the thumbnail
        #temp_handle = StringIO()
        #image.save(temp_handle, 'png')
        #temp_handle.seek(0)

        # Save to the thumbnail field
        #suf = SimpleUploadedFile(os.path.split(self.photo.name)[-1],
         #       temp_handle.read(), content_type='image/png')
        #self.thumbnail.save(suf.name+'.png', suf, save=False)

        # Save this photo instance
        #super(Photo, self).save()
    def __unicode__(self):
        return self.titolo





class Riferimenti(models.Model):
    riferimento=models.CharField(max_length=50)
    content_type=models.ForeignKey(ContentType,blank=True)
    object_id = models.CharField(max_length=30,blank=True)
    content_object = GenericForeignKey("content_type", "object_id" )
    def __unicode__(self):
        return self.riferimento



class Valori(models.Model):
    valore=models.CharField(max_length=50,primary_key=True)
    def __unicode__(self):
        return self.valore

class TipoCampo(models.Model):
    tipo=models.CharField(max_length=40,primary_key=True)
    html=models.TextField()
    def decodeHtml(self):
        list=[]
        pattern = re.compile(r'\(\w+\)')
        html=self.html
        lista = findall(pattern, html)
        for i in lista:
            list.append(i.strip('(').strip(')'))
        list = dict.fromkeys(list).keys()
        return html , list
    def __unicode__(self):
        return self.tipo
    class Meta:
        verbose_name_plural = "Tipo Campi"

class Campo(models.Model):
    titolo=models.CharField(max_length=30)
    valori=models.ManyToManyField('self',through='ValoriCampo',symmetrical=False,related_name='Valori',blank=True)
    tipo=models.ForeignKey(TipoCampo)
    def __unicode__(self):
        return u"%s" " " u"--%s--" % (self.titolo,self.tipo)
    class Meta:
        verbose_name_plural = "Campi"
    def campoHtml(self,oggetto,lav,padre,campo,rMap):
        html_fg=''
        map={}
        tipoCampo=self.tipo
        ht=tipoCampo.decodeHtml()
        html=ht[0]
        val=ht[1]
        pad_rif=self.Campo_padre.filter(componente=Riferimenti.objects.get(riferimento=oggetto))
        figli=[]
        if(pad_rif):
                for y in pad_rif:
                    figli.append(y.figlio)
                figli = dict.fromkeys(figli).keys()
        for i in val:
            if(i=='id'):
                map[i]=self.id
            elif(i=='titolo'):
                map[i]=self.titolo
            elif(i=='oggetto'):
                map[i]=oggetto
            elif(i=='lav'):
                if(lav):
                    map[i]='lav = '+str(lav).replace(' ' ,'_')
                else:
                    map[i]=''
            elif(i=='padre'):
                 if(padre):
                    map[i]='padre = '+str(padre)
                 else:
                    map[i]=''
            elif(i=='specifica'):
                spec=self.specifica_set.all()
                if(spec):
                    map[i]='specifica ='+str(spec[0].id)
                else:
                    map[i]=''
            elif(i=='specifiche'):
                pass
            elif(i=='value'):
                if(padre):
                    mappa=MappaCampi.objects.get(campo=padre,figlio=self,valore_padre=campo)
                    #if(self==mappa.figlio and mappa.valore_padre==campo):
                    map[i]=str(mappa.valore_figlio)
                else:
                    map[i]=''
            elif(i=='stato'):
                if(padre):
                    mappa=MappaCampi.objects.get(campo=padre,figlio=self,valore_padre=campo)
                    #if(self==mappa.figlio and mappa.valore_padre==campo):
                    if(mappa.non_editabile):
                        map[i]='disabled'
                    else:
                        map[i]='enabled'
                else:
                    map[i]='enabled'
            elif(i=='figli'):
                if(figli):
                    for index,item in enumerate(figli):
                        if(index==0):
                            fg_id=str(item.id)
                        else:
                            fg_id=fg_id+';'+str(item.id)
                    map[i]='figli ='+fg_id
                else:
                    map[i]=''
            elif(i=='option'):
                option=''
                valori=self.valoricampo_set.all().filter(Q(rif_componente=Riferimenti.objects.get(riferimento=oggetto))|Q(rif_componente=None))
                if(figli):
                    for z in figli:
                        html_fo=z.campoHtml(oggetto,lav,pad_rif[0].campo_id,valori[0],False)
                        html_fg=html_fg+html_fo
                if(rMap):
                    for x in valori:
                        a= "<option value='%s'>%s</option>"%(str(x.valori_id),str(x.valori_id))
                        option=option+a

                else:
                    valori=[]
                    mappa=self.Campo_figlio.all()
                    for t in mappa:
                        if(self==t.figlio and t.valore_padre==campo):
                            valori.append(t.valore_figlio)
                    for x in valori:
                        a= "<option value='%s'>%s</option>"%(str(x),str(x))
                        option=option+a
                map[i]=option
            elif(i=='image'):
                img=''
                frt=''
                default=''
                im=self.valoricampo_set.all().filter(Q(rif_componente=Riferimenti.objects.get(riferimento=oggetto))|Q(rif_componente=None))
                spec=self.specifica_set.all()
                titolo=self.titolo
                id=self.id
                fg_id=''
                if(figli):
                    fg_id='figli ='
                    for z in figli:
                        fg_id=fg_id+str(z.id)
                        html_fo=z.campoHtml(oggetto,lav,pad_rif[0].campo_id,im[0],False)
                        html_fg=html_fg+html_fo
                if(spec):
                    specifica='specifica ='+str(spec[0].id)
                else:
                    specifica=''
                for x in im:
                    obj=x.riferimento.get().content_object
                    if (hasattr(obj,'spec1')and obj.spec1):
                        frt=str(obj.spec1.id)+'='+str(obj.valore_1)
                        if(obj.valore_1==0):
                            default='default=true'
                        else:
                            default='default=false'
                    if(hasattr(obj,'spec2')and obj.spec1):
                        frt=frt+' '+str(obj.spec2.id)+'='+str(obj.valore_2)+' sclass="formati"'
                        if(obj.valore_1==0):
                            default='default=true'
                        else:
                            default='default=false'
                    if(hasattr(obj,'default') ):
                            if(obj.default==True):
                                default='default=true'
                            else:
                                default='default=false'

                    a='<label class="checkbox-inline"> <input type="radio" class="campo" oggetto="%s"  %s  name="%s" ' \
                      ' id="%s" %s %s  value="%s" %s %s %s ><img src="/static/media/%s" alt="option1" >%s</label>'\
                      %(oggetto,specifica,titolo,id,lav,padre,str(x.valori),frt,default,fg_id,str(x.immagine.image),str(x.valori))
                    img=img+a
                map[i]=img
            else:
                map[i]=''
        html=html % map
        html=html+html_fg
        return html


#class ValoriCampoQueryset(models.QuerySet):
 #   def Valori_campo(self):
  #      return self.filter(campo='padre')
#class ValoriCampoManager(models.Manager):
 #   def get_queryset(self):
  #      return ValoriCampoQueryset(self.model)
   # def Valori_campo(self):
    #    return self.get_queryset().Valori_campo()

class ValoriCampo(models.Model):
    campo=models.ForeignKey(Campo)
    immagine=models.ForeignKey(Immagini,null=True,blank=True)
    valori=models.ForeignKey(Valori)
    riferimento=models.ManyToManyField(Riferimenti,blank=True,null=True)
    rif_componente=models.ForeignKey(Riferimenti,related_name='Componente',null=True,blank=True)
    def __unicode__(self):
        return str(self.valori)


class ImmaginiCampo(models.Model):
    campo=models.ForeignKey(Campo,blank=True,null=True)
    image=models.ImageField()
    valori=models.ForeignKey(Valori)
    riferimento=models.ForeignKey(Riferimenti,blank=True,null=True)
    rif_componente=models.ForeignKey(Riferimenti,related_name='Im_Componente',null=True,blank=True)

class MappaCampi(models.Model):
    campo=models.ForeignKey(Campo,related_name='Campo_padre')
    valore_padre=models.ForeignKey(ValoriCampo,related_name="Valore") #,limit_choices_to = {'campo':'1'}
    figlio=models.ForeignKey(Campo,related_name='Campo_figlio')
    valore_figlio=models.ForeignKey(Valori)
    non_editabile=models.BooleanField(default='False')
    componente=models.ForeignKey(Riferimenti,related_name='Rif_Componente',null=True,blank=True)
    mappa={}
    def valFigli(self):
        mappa={}
        val=[]
        mappa['campo']=self.figlio_id
        mappa=self.valore_figlio
        return mappa

    def save(self, *args, **kwargs):
         self.componente=self.valore_padre.rif_componente
         componente=self.valore_padre.rif_componente.content_object
         map=componente.campicomponente_set
         padre=map.get_or_create(componente=componente,campo=self.campo)
         figlio=map.get_or_create(componente=componente,campo=self.figlio)
         valFiglio=ValoriCampo.objects.get_or_create(campo=self.figlio,valori=self.valore_figlio,rif_componente=self.valore_padre.rif_componente)
         padre[0].padri=True
         padre[0].save()
         figlio[0].figli=True
         figlio[0].save()
         valFiglio[0].save()
         super(MappaCampi,self).save(*args, **kwargs)

    def delete(self,*args,**kwargs):
        componente=self.valore_padre.rif_componente.content_object
        map=componente.campicomponente_set
        campo=map.get(componente=componente,campo=self.figlio)
        if(map.filter(componente=componente,campo=self.campo).count()<2):
            padre=map.get(componente=componente,campo=self.campo)
            padre.padri=False
            padre.save()
        campo.delete()
        super(MappaCampi,self).delete(*args, **kwargs)

