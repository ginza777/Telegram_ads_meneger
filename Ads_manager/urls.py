"""
URL configuration for Ads_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from Ads_manager.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('channels/json/', channels_to_json, name='channels_to_json'),
    path('client_settings/json/', client_settings_to_json, name='client_settings_to_json'),
    path('bot/json/', bot_to_json, name='bot_to_json'),
    path('channel_type/json/', channel_type_to_json, name='channel_type_to_json'),
    path('keyword/json/', keyword_channel_ads_to_json, name='keyword_to_json'),
    path('config/url/list/json/',all_url_list_html, name='all_url_list_html'),


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)