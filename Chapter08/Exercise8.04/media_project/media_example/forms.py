from django import forms


class UploadForm(forms.Form):
    file_upload = forms.FileField()
