"""indrz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import login, logout
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import javascript_catalog
# from maps import views as map_view

js_info_dict = {
    'domain': 'djangojs',
    'packages': ('maps', 'poi_manager', ),
}


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'maps.views.view_map'),  # homepage start page url
    url(r'^i18n/', include('django.conf.urls.i18n')),

    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),

    url(r'^api/v1/', include('api.urls')),
    url(r'^api/v1/docs/', include('rest_framework_swagger.urls')),
    url(r'^map/', include('maps.urls')),
    url(r'^poi/', include('poi_manager.urls')),
    url(r'^wu/', include('homepage.urls')),

]

urlpatterns += i18n_patterns(
    url(r'^$', 'maps.views.view_map'),  # homepage start page url
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),

    url(r'^api/v1/', include('api.urls')),
    url(r'^map/', include('maps.urls')),
    url(r'^poi/', include('poi_manager.urls')),
    url(r'^jsi18n/$', javascript_catalog, js_info_dict,
        name='javascript-catalog'),
)


urlpatterns += [
    # ... the rest of your URLconf goes here ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        url(r'^rosetta/', include('rosetta.urls')),
    ]
