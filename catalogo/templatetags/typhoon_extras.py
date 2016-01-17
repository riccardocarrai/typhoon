from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()


@register.filter(name='cut')
def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, '')


@register.filter(name='breadcrumbs')
def breadcrumbs(url):
    links=url.strip('/').split('/')
    home = ['<li><a href="/"><span class="glyphicon glyphicon-home"></span></a></li>',]
    bread = []
    total = len(links)-1
    for i, link in enumerate(links):
        if not link == '':
            bread.append(link)
            this_url = "/".join(bread)
            sub_link = re.sub('-', ' ', link)
            if not i == total:
                tlink = '<li><a href="/%s/" title="Breadcrumb link to %s">%s</a></li>' % (this_url.title(), sub_link.title(), sub_link.title())
            else:
                tlink = '<li class="active">%s</li>' % sub_link.title()
            home.append(tlink)
    bcrumb = "".join(home)
    return mark_safe(bcrumb)
