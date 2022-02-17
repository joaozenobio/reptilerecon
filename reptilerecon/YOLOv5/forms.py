from django.forms import ModelForm
from django import forms
from .models import Video
from django.utils.safestring import mark_safe
from django.forms import widgets


class UploadVideoForm(ModelForm):
    class Meta:
        model = Video
        fields = ['video']
        widgets = {
            'video': forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control'})
        }
