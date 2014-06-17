from django.conf.urls import patterns, url
from corpora import views

urlpatterns = patterns('',
    # /compute/
    url(r'^$', views.compute_index, name='index'),
    # /compute/result
    url(r'result/$', views.compute_result, name='result'),
                   )
