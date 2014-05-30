from django.conf.urls import patterns, url
from corpora import views

urlpatterns = patterns('',
    # /corpora/
    url(r'^$', views.corpora_index, name='index'),
    # /corpora/2
    url(r'(?P<corpus_id>\d+)/$', views.corpus_detail, name='detail'),               )