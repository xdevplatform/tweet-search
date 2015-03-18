from django.conf.urls import patterns, include, url

from django.views.generic.base import TemplateView, RedirectView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^home$', 'home.views.home', name='home'),
    url(r'^query/chart', 'home.views.query_chart', name='query_chart'),
    url(r'^query/tweets', 'home.views.query_tweets', name='query_tweets'),
    url(r'^logout$', 'home.views.logout', name='logout'),
    url(r'^login$', 'home.views.login', name='login'),

    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/bird.ico')),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt')),

    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^admin/', include(admin.site.urls)),
)
