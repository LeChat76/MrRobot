from django.shortcuts import render
from .models import Project


def project_list(request):
    projects = Project.objects.all().prefetch_related('skill', 'technology').order_by('project_number')
    return render(request, 'openclassrooms.html', {'projects': projects})

