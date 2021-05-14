from django import forms
# from .models import Data


class UploadFileForm(forms.Form):
    # title = forms.CharField(max_length=50)
    file = forms.FileField(widget=forms.ClearableFileInput())
