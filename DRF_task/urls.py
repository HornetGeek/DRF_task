"""DRF_task URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view

schema_view = swagger_get_schema_view(
    openapi.Info(
        title="api documents",
        default_version='1.0.0',
        description="Api for client and employee"
    ),
    public=True
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("core.urls")),
    path('api/v1/',
    include([
        path('api/', include(("core.urls",'core'), namespace='api')),
        path('swagger/schema/',schema_view.with_ui('swagger',cache_timeout=0),name="swagger-schema")
    ]))
]
