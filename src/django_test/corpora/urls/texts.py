from django.conf.urls import patterns, url

from corpora import views

urlpatterns = patterns('',
    # /texts/
    url(r'^$', views.text_index, name='index'),
    # /texts/3/
    url(r'(?P<text_id>\d+)/$', views.text_detail, name='detail'),
    )
