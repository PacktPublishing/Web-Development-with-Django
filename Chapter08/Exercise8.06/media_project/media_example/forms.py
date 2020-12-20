from django import forms


class UploadForm(forms.Form):
    image_upload = forms.ImageField()
    file_upload = forms.FileField()
