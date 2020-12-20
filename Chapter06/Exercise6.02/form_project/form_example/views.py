from django.shortcuts import render


def form_example(request):
    for name in request.POST:
        print("{}: {}".format(name, request.POST.getlist(name)))

    return render(request, "form-example.html", {"method": request.method})
