from django.contrib import admin

# Register your models here.

from anagrafiche.models import *

class GiorniFestiviInlines(admin.TabularInline):
    model = GiorniFestivi

class voce_rubricaInlines(admin.TabularInline):
    model = voce_rubrica

class rubricaOption(admin.ModelAdmin):
    inlines=[voce_rubricaInlines,]

class paeseOption(admin.ModelAdmin):
    filter_horizontal =('continente')

class indirizziInlines(admin.TabularInline):
    model = indirizzo_mycontact
class dipendentiInlines(admin.TabularInline):
    model = referente

class clientiOption(admin.ModelAdmin):
    inlines = [indirizziInlines,dipendentiInlines]

class macchinaOption(admin.ModelAdmin):
    radio_fields = {'funzione':admin.HORIZONTAL}

class GiorniFestivitaOption(admin.ModelAdmin):
    fieldsets = ((None,{'fields':(('giorno','mese'),'festivita')}),)
    list_display = ('giorno','mese','festivita')

admin.site.register(contatto)
admin.site.register(cliente,clientiOption)
admin.site.register(impiegati)
admin.site.register(macchina,macchinaOption)
admin.site.register(indirizzo)
admin.site.register(paese)
admin.site.register(continente)
admin.site.register(tipo_societa)
admin.site.register(provincia)
admin.site.register(indirizzo_mycontact)
admin.site.register(rubrica,rubricaOption)
admin.site.register(GiorniFestivi,GiorniFestivitaOption)