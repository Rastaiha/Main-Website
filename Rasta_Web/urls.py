"""Rasta_Web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include

import Rasta_Web
from apps.doc.views import doc_downloader
from apps.intro import urls as intro_urls
from apps.doc import urls as doc_url
from apps.contact_us import urls as contact_us_urls
from apps.blog import urls as blog_url
from apps.events import urls as events_url
from apps.newsletter import urls as newsletter_url
from apps.shortener import urls as shortener_urls
from apps.members import urls as members_urls
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin_chi/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('contact_us/', include(contact_us_urls)),
    path('events/', include(events_url)),
    path('blog/', include(blog_url)),
    path('download/', doc_downloader),
    path('newsletter/', include(newsletter_url)),
    path('doc/', include(doc_url)),
    path('', include(intro_urls)),
    path('go/', include(shortener_urls)),
    path('members/',include(members_urls))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

handler404 = 'Rasta_Web.views.handler404'
