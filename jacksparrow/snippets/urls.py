from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

urlpatterns = [
    url(r'^snippets/$', views.snippet_list),
    url(r'^snippets/(?P<pk>[0-9]+)$', views.snippet_detail),
    url(r'^snippets/last/(?P<liste_ville>[\w\,\'\[\]\.\-\%0-9]+)/(?P<iterations_temperature>[0-9]+)$', views.snippet_last),
]

urlpatterns = format_suffix_patterns(urlpatterns)
