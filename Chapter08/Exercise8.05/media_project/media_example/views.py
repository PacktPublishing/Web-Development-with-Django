import os
from PIL import Image
from django.conf import settings
from django.shortcuts import render

from .forms import UploadForm


def media_example(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            save_path = os.path.join(settings.MEDIA_ROOT, form.cleaned_data["file_upload"].name)

            image = Image.open(form.cleaned_data["file_upload"])
            image.thumbnail((50, 50))
            image.save(save_path)
    else:
        form = UploadForm()

    return render(request, "media-example.html", {"form": form})
