from django.shortcuts import render

def index(request):
    names = "john,doe,mark,swain"
    return render(request, "index.html", {'names': names})
