from django.shortcuts import render
from .forms import OrderForm


def form_example(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
    else:
        form = OrderForm()

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            for name, value in form.cleaned_data.items():
                print("{}: ({}) {}".format(name, type(value), value))

    return render(request, "form-example.html", {"method": request.method, "form": form})
