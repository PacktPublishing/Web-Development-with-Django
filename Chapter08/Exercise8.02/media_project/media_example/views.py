from django.shortcuts import render

def media_example(request):
    return render(request, "media-example.html")
