from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import OpenclassroomsProjectList


app_name = 'openclassrooms'

urlpatterns = [
    path('', OpenclassroomsProjectList, name='OpenclassroomsProjectList'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
