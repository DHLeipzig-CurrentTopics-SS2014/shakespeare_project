from django.conf.urls import patterns, url

from corpora import views

urlpatterns = patterns('',
    # /authors/
    url(r'^authors/$', views.author_index, name='index'),
    # /authors/3/
    url(r'^authors/(?P<author_id>\d+)/$', views.author_detail, name='detail'),
    
    # /texts/
    url(r'^texts/$', views.text_index, name='index'),
    # /texts/3/
    url(r'^texts/(?P<text_id>\d+)/$', views.text_detail, name='detail'),
    # /texts/3/words
    url(r'^texts/(?P<text_id>\d+)/words/$', views.text_words, name='words'),
    
    # /corpora/
    url(r'^corpora/$', views.corpora_index, name='index'),
    
    # /corpora/
    url(r'^corpora/upload/$', views.corpora_upload, name='upload'),
    
        
    )
    
