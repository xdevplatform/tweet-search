from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from app import settings
from home import views

urlpatterns = patterns('',
    url(r'^$', views.login, name='login'),
    url(r'^home$', views.home, name='home'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^query/chart', views.query_chart, name='query_chart'),
    url(r'^query/tweets', views.query_tweets, name='query_tweets'),
    url(r'^query/frequency', views.query_frequency, name='query_frequency'),

    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^admin/', admin.site.urls),
)

urlpatterns += patterns('',
 (r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
 )