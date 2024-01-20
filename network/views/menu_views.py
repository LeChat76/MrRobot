from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def menu_view(request):
    return render(request, 'network_menu.html')