from django.conf.urls import patterns, url
from calculations import views


urlpatterns = patterns('', 
    # /calculations/
    url(r'^$', views.index, name='index'),
    
        
    )