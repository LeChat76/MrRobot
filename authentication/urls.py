from django.urls import path
import authentication.views as authentication

app_name = 'authentication'
urlpatterns = [
    path('login/', authentication.login_page, name='login_view'),
]
