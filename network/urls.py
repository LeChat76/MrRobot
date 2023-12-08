from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import VlanView, VlanDeleteView

app_name = 'network'
urlpatterns = [
    path('vlan/', VlanView.as_view(), name='VlanView'),
    path('vlan/delete/<int:pk>/', VlanDeleteView.as_view(), name='vlan_delete'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
