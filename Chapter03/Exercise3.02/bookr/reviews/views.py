from django.shortcuts import render


def simple_template_view(request):
    return render(request, 'base.html')
