from django import forms
from .models import UploadedData

class UploadDataForm(forms.ModelForm):
    class Meta:
        model = UploadedData
        fields = ['file']