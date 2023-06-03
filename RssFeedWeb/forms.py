from django import forms
from .models import subsData

class SubscribeForm(forms.ModelForm):
    class Meta:
        model = subsData
        fields = ['link', 'date']
        exclude = ['date']
        widgets = {
            'date': forms.DateTimeInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['link'].required = False  # link 필드를 선택 사항으로 설정