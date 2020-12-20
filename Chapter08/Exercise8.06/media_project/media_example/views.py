from django.shortcuts import render

from .forms import UploadForm
from .models import ExampleModel


def media_example(request):
    instance = None

    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():
            instance = ExampleModel()
            instance.image_field = form.cleaned_data["image_upload"]
            instance.file_field = form.cleaned_data["file_upload"]
            instance.save()
    else:
        form = UploadForm()

    return render(request, "media-example.html", {"form": form, "instance": instance})
