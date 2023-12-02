from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import project_list
# from django.http import HttpResponse

# def no_favicon(request):
#     return HttpResponse(status=204)

app_name = 'projects'
urlpatterns = [
    path('', project_list, name='project_list'),
    # path('favicon.ico', no_favicon),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
