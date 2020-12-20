from django.shortcuts import render


def form_example(request):
    return render(request, "form-example.html")
