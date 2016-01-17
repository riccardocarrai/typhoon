
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline,GenericStackedInline
from prodotti.models import *
from catalogo.admin import *
from django import forms


# Register your models here.
class CampoComponenteInline(admin.TabularInline):
    model = CampiComponente
    suit_classes = 'suit-tab suit-tab-campi'
class ImmaginiInlines(GenericStackedInline):
    model = Immagini
    suit_classes = 'suit-tab suit-tab-immagini'
class AccessoriInLines(admin.TabularInline):
    model = Accessori
    fk_name = 'from_componente'
    suit_classes = 'suit-tab suit-tab-accessori'
class ConversioneInLine(admin.TabularInline):
    model = conversione

class GiorniAumentoInline(GenericTabularInline):
    model = GiorniAumento
    suit_classes = 'suit-tab suit-tab-giorni'
class LavorazioneComponenteInline(admin.StackedInline):
    model = LavorazioneComponente
    fieldsets=[   ('',{
                 'classes':('suit_tab','suit-tab-varianti',),
            'fields':[('lavorazione','tipoLavorazione'),('prezzoVendita','calcolo_prezzo'),('spec1','valore_1'),('spec2','valore_2'),('campo','valore_campo')]
    }),
    ]
    suit_classes = 'suit-tab suit-tab-lavorazioni'
    def formfield_for_dbfield(self, field, **kwargs):
     if field.name == 'materiale':
        componente=self.get_object(kwargs['request'], Componente)
        materiale = VarianteComponente.objects.filter(componente=componente)
        return forms.ModelChoiceField(queryset=materiale,required=False)
     return super(LavorazioneComponenteInline, self).formfield_for_dbfield(field, **kwargs)

    def get_object(self, request, model):
        object_id = request.META['PATH_INFO'].strip('/').split('/')[-1]
        try:
            object_id =object_id
        except ValueError:
            return None
        return model.objects.get(pk=object_id)

class caratteristicheInlines(GenericTabularInline):
    model = caratteristica
    suit_classes = 'suit-tab suit-tab-caratteristica'

class VarianteComponenteInline(admin.StackedInline):
    model = VarianteComponente
    inlines=[caratteristicheInlines]
    fieldsets=[   ('',{
                 'classes':('suit_tab','suit-tab-varianti',),
            'fields':['variante',('prezzoVendita','calcolo_prezzo'),('spec1','valore_1'),('spec2','valore_2'),('campo','valore_campo'),'default']
    }),
                  ('',{
                 'classes':('suit_tab','suit-tab-caratteristica',),
            'fields':[]
    }),
                  ]
    suit_form_tabs = (('varianti', 'Varianti'),('caratteristica', 'Caratteristica'))
    suit_classes = 'suit-tab suit-tab-varianti'
class ScontoFormatoInlines(admin.TabularInline):
    model = ScontoFormato
    suit_classes = 'suit-tab suit-tab-formati'
class LavorazioneAdmin(admin.ModelAdmin):
    fieldsets = ((None,{'fields':('nome',('costo','UM'),('macchina','addetti'))}),)


#class varianteComponenteOption(admin.ModelAdmin):
 #   inlines = [caratteristicheInlines,]

class ProdottoOption(admin.ModelAdmin):
    inlines = [ImmaginiInlines]
    filter_horizontal = ('Componenti',)


class ComponenteOption(admin.ModelAdmin):
    inlines = [ImmaginiInlines,VarianteComponenteInline,LavorazioneComponenteInline,ScontoFormatoInlines,
               AccessoriInLines,GiorniAumentoInline,CampoComponenteInline]
    #filter_horizontal = ('varianti',)
    fieldsets = [
        ('',{
                 'classes':('suit_tab','suit-tab-generale',),
            'fields':['nome','descrizione']
    }),
        ('',{
                 'classes':('suit_tab','suit-tab-immagini',),
            'fields':[]
    }),
        ('',{
                 'classes':('suit_tab','suit-tab-varianti',),
            'fields':[]
    }),
        ('',{
                 'classes':('suit_tab','suit-tab-lavorazioni',),
            'fields':[]
    }),
        ('',{
                 'classes':('suit_tab','suit-tab-giorni',),
            'fields':[]
    }),
        ('',{
                 'classes':('suit_tab','suit-tab-formati',),
            'fields':[]
    }),
           ('',{
                 'classes':('suit_tab','suit-tab-accessori',),
            'fields':[]
    }),
              ('',{
                 'classes':('suit_tab','suit-tab-campi',),
            'fields':[]
    }),
    ]
    suit_form_tabs = (('generale', 'Generale'),('immagini','Immagini'),('varianti','Varianti'),('lavorazioni','Lavorazioni'),
                      ('giorni','Giorni'),('formati','Formati'),('accessori','Accessori'),('campi','Campi'))
class varianteOption(admin.ModelAdmin):
    search_fields = ('nome',)
    inlines = [ImmaginiInlines,caratteristicheInlines]
    #fieldsets = ((None,{'fields':('nome',('costo','UM'))}),)
    fieldsets = [
         ('',{
                 'classes':('suit_tab','suit-tab-generale',),
            'fields':['nome',('costo','UM')]
    }),
        ('',{
                 'classes':('suit_tab','suit-tab-caratteristica',),
            'fields':[]
    }),
    ]
    suit_form_tabs = (('generale', 'Generale'),('caratteristica', 'Caratteristica'))

class FormatoAdmin(admin.ModelAdmin):
    inlines = [ImmaginiInlines]
    fieldsets = ((None,{'fields':('nome',('spec1','valore_1'),('spec2','valore_2'))}),)

class SpecificaAdmin(admin.ModelAdmin):
    filter_horizontal = ('campo',)

class CalcoloUmAdmin(admin.ModelAdmin):
    inlines = [ConversioneInLine]


admin.site.register(UM)
admin.site.register(Componente,ComponenteOption)
admin.site.register(Lavorazione,LavorazioneAdmin)
admin.site.register(Prodotto,ProdottoOption)
admin.site.register(variante,varianteOption)
admin.site.register(Specifica,SpecificaAdmin)
admin.site.register(Formati,FormatoAdmin)
admin.site.register(Riferimenti)
admin.site.register(calcoloUm,CalcoloUmAdmin)
