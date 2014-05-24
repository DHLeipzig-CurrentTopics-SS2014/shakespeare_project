from django.conf.urls import patterns, url

from corpora import views

urlpatterns = patterns('',
    # /authors/
    url(r'^$', views.author_index, name='index'),
    # /authors/3/
    url(r'(?P<author_id>\d+)/$', views.author_detail, name='detail'),
    )
