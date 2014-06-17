from django.conf.urls import patterns, url
from corpora import views
from corpora.view import compute_result as ce

urlpatterns = patterns('',
    # /compute/
    url(r'^$', views.compute_index, name='index'),
    # /compute/result
    url(r'result/$',ce.compute_result, name='result'),
                   )
