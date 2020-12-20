from django.shortcuts import render

from .forms import UploadForm


def media_example(request):
    instance = None

    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():
            instance = form.save()
    else:
        form = UploadForm()

    return render(request, "media-example.html", {"form": form, "instance": instance})
