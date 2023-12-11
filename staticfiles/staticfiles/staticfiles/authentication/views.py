# authentication/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate

from .forms import authentication_form as authentication


def login_page(request):
    form = authentication.LoginForm()
    message = ''
    if request.method == 'POST':
        form = authentication.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('network:vlan_view')
            else:
                message = 'Identifiants invalides.'
    return render(
        request,
        'login.html',
        context={'form': form, 'message': message}
    )

def logout_user(request):
    logout(request)
    return redirect('login')
