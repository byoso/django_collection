"""
URL configuration for _project project.

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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_home.urls', namespace='home')),
    path('', include('_adminplus.urls', namespace='_adminplus')),
    path('app_cdn/', include('app_cdn.urls', namespace="cdn")),
    path('app_site/', include('app_site.urls', namespace="site")),

    # AUTHENTICATION URLS
    # path('accounts/', include('allauth.urls')),  # allauth
    path('', include('_quick_auth.urls')),
    # only if you want to try the demo at path '/':
    # path('', TemplateView.as_view(template_name='auth/demo.html')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
