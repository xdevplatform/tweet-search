from django.conf.urls import patterns, include, url

from app import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'home.views.login', name='login'),
    url(r'^home$', 'home.views.home', name='home'),
    url(r'^logout$', 'home.views.logout', name='logout'),
    url(r'^query/chart', 'home.views.query_chart', name='query_chart'),
    url(r'^query/tweets', 'home.views.query_tweets', name='query_tweets'),

    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
 (r'^static/(?P.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
 )
