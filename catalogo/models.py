from django.db import models
from django.db import connection
from anagrafiche.models import *
from prodotti.models import *
from itertools import islice, chain
from catalogo.media import *

# Create your models here.



class categoriaManager(models.Manager):
    def returnProdotti(self):
            #map_name={'categoria':'categoria','prodotto':'prodotto'}
            #cursor=connection.cursor()
            #cursor.execute("SELECT catalogo_categoria.categoria, catalogo_categoria_prodotti.prodotto_id "
             #              "FROM catalogo_categoria LEFT OUTER JOIN catalogo_categoria_prodotti "
             #              "WHERE catalogo_categoria.id=catalogo_categoria_prodotti.categoria_id")

            result_list=categoria.objects.values('categoria','prodotti')
            for prodotto in result_list:
                Prodotto.objects.filter()
            #for row in cursor.fetchall():
             #   c=self.model(categoria=row[0])
              #  result_list.append(c)
            return result_list

class QuerySetChain(object):
    """
    Chains multiple subquerysets (possibly of different models) and behaves as
    one queryset.  Supports minimal methods needed for use with
    django.core.paginator.
    """

    def __init__(self, *subquerysets):
        self.querysets = subquerysets

    def count(self):
        """
        Performs a .count() for all subquerysets and returns the number of
        records as an integer.
        """
        return sum(qs.count() for qs in self.querysets)

    def _clone(self):
        "Returns a clone of this queryset chain"
        return self.__class__(*self.querysets)

    def _all(self):
        "Iterates records in all subquerysets"
        return chain(*self.querysets)

    def __getitem__(self, ndx):
        """
        Retrieves an item or slice from the chained set of results from all
        subquerysets.
        """
        if type(ndx) is slice:
            return list(islice(self._all(), ndx.start, ndx.stop, ndx.step or 1))
        else:
            return islice(self._all(), ndx, ndx+1).next()






class categoria(models.Model):
    categoria=models.CharField(max_length=20)
    descrizione = models.TextField(blank=True)
    short_description=models.TextField(blank=True)
    immagini=models.ManyToManyField(Immagini,blank=True)
    small_image= models.ImageField(blank=True)
    in_evidenza = models.BooleanField(default=False)
    prodotti=models.ManyToManyField(Prodotto, blank=True)
    objects = categoriaManager()
    def get_absolute_url(self):
        return "/%s/" % self.categoria
    class Meta:
        verbose_name_plural = "Categorie"
    def __unicode__(self):
        return self.categoria
    #def __unicode__(self):              # __unicode__ on Python 2
     #   return "%s (%s)" % (self.categoria, ", ".join([Prodotto.prodotto
      #                                            for Prodotto in self.prodotti.all()]))



class rigaOrdine(models.Model):
    nr=models.AutoField(primary_key=True)
    articolo=models.ForeignKey(Prodotto)
    data_consegna=models.DateField()


class Ordine(models.Model):
    Nr=models.AutoField(primary_key=True)
    cliente=models.ForeignKey(contatto)
    righe=models.ForeignKey(rigaOrdine)



#class specifica(models.Model):
 #   ordine=models.ForeignKey(rigaOrdine)
  #  valore=models.CharField(max_length=10)

