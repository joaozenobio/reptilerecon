from django.forms import ModelForm
from django import forms
from .models import Video


class UploadVideoForm(ModelForm):
    class Meta:
        model = Video
        fields = ['video']
        widgets = {
            'video': forms.ClearableFileInput(attrs={'multiple': True})
        }
