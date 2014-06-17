from django.conf.urls import patterns, url
from corpora import views

urlpatterns = patterns('',
    # /compute/
    url(r'^$', views.compute_index, name='index'),
    # /compute/erg
    url(r'erg/$', views.compute_erg, name='results'),
                   )
