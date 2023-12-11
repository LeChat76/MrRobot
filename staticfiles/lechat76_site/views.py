# lechat76_site/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import logout

def main(request):
    return render(request, 'main.html')

def logout_user(request):
    logout(request)
    return redirect('authentication:login_view')