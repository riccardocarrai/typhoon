from django.contrib import admin
from catalogo.models import *
from catalogo.media import *
from django import forms
from django.contrib.contenttypes.admin import GenericTabularInline
from prodotti.models import *


# Register your models here.

#class MappaCampiAdminForm(forms.ModelForm):
 #   class Meta:
  #      model=MappaCampi


   # def __init__(self, *args, **kwargs):
    #    super(MappaCampiAdminForm, self).__init__(*args, **kwargs)
     #   if self.instance.id and self.instance.ValoriCampo:
      #      q = Q(active=True)| Q(id=self.instance.ValoriCampo.id)
       #     self.fields['ValoriCampo'].queryset = ValoriCampo.objects.filter(q)
        #else:
         #   self.fields['ValoriCampo'].queryset = ValoriCampo.objects.filter(active=True)


class immaginiInlines(admin.TabularInline):
    model = ImmaginiCampo

class ImmaginiInlines(GenericTabularInline):
    model = Immagini
    #exclude = ('titolo',)

class ValoriCampoInlines(admin.TabularInline):
    model = ValoriCampo
    filter_vertical = ('riferimento',)

class MappaCampiInlines(admin.TabularInline):
    model = MappaCampi
    fk_name = 'campo'

    def formfield_for_dbfield(self, field, **kwargs):
     if field.name == 'valore_padre':
        campo=self.get_object(kwargs['request'], Campo)
        valori = ValoriCampo.objects.filter(campo=campo)
        return forms.ModelChoiceField(queryset=valori)
     return super(MappaCampiInlines, self).formfield_for_dbfield(field, **kwargs)

    def get_object(self, request, model):
        object_id = request.META['PATH_INFO'].strip('/').split('/')[-1]
        try:
            object_id = int(object_id)
        except ValueError:
            return None
        return model.objects.get(pk=object_id)

class categoriaOption(admin.ModelAdmin):
    filter_horizontal = ('prodotti', 'immagini')

#class MappaCampiAdmin(admin.ModelAdmin):
 #   form=MappaCampiAdminForm

class CampoAdmin(admin.ModelAdmin):
    list_display = ('titolo','tipo')
    inlines = [ValoriCampoInlines, MappaCampiInlines]


class ImmaginiAdmin(admin.ModelAdmin):
    exclude = ['content_type','object_id']


admin.site.register(categoria,categoriaOption)
admin.site.register(media)
admin.site.register(Immagini,ImmaginiAdmin)
admin.site.register(TipoOggetto)
admin.site.register(Campo,CampoAdmin)
admin.site.register(TipoCampo)
admin.site.register(Valori)
admin.site.register(MappaCampi)
