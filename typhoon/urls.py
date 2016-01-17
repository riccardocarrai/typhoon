from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from anagrafiche.views import registrazione
from prodotti.views import *




urlpatterns = patterns('',
    # Examples:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'catalogo.views.index', name='index'),
    url(r'^accounts/login/$', 'catalogo.views.login'),
    url(r'^accounts/auth/$', 'catalogo.views.auth_view'),
    url(r'^logout/$','catalogo.views.logoutWiews'),
    url(r'^registrazione/$', registrazione.as_view()),
    url(r'^registrazione/validate',registrazione.as_view() ),
    url(r'^preventivo/$',ViewsPreventivo.as_view()),
    url(r'^(\w+|\w+-\w+|\w+-\w+-\w+|\w+-\w+-\w+-\w+)/$',ViewsCategorie.as_view(),name='categoria'),
    url(r'^(\w+|\w+-\w+|\w+-\w+-\w+|\w+-\w+-\w+-\w+)/(\w+|\w+-\w+|\w+-\w+-\w+|\w+-\w+-\w+-\w+)/$',ViewsProdotti.as_view(),name='prodotti'),
    url(r'^(\w+|\w+-\w+|\w+-\w+-\w+|\w+-\w+-\w+-\w+)/(\w+|\w+-\w+|\w+-\w+-\w+|\w+-\w+-\w+-\w+)/(\w+|\w+-\w+|\w+-\w+-\w+|\w+-\w+-\w+-\w+)$',ViewsPreventivo.as_view(),name='materiale'),

    # url(r'^blog/', include('blog.urls')),


)

if settings.DEBUG:
        urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
