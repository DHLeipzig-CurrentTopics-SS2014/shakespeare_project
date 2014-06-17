from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wordtracer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^authors/', include('corpora.urls.authors')),
    url(r'^texts/', include('corpora.urls.texts')), 
    url(r'^compute/', include('corpora.urls.compute'))

)
