"""
URL configuration for lechat76_site project.

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
from .views import main, logout_user
from openclassrooms.views import OpenclassroomsProjectList


app_name = 'lechat76_site'

urlpatterns = [
    path('', OpenclassroomsProjectList, name='OpenclassroomsProjectList'),
    path('admin/', admin.site.urls),
    path('main/', main, name='main'),
    path('logout_user/', logout_user, name='logout_user'),
    path('openclassrooms/', include('openclassrooms.urls')),
    path('network/', include('network.urls')),
    path('authentication/', include('authentication.urls')),
]
