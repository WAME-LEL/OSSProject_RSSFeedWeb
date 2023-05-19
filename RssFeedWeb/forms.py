from django import forms
from .models import subsData

class SubscribeForm(forms.ModelForm):
    class Meta:
        model = subsData
        fields = ['link']