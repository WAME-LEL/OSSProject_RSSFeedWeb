from django import forms
from .models import subsData
from .models import scrapData

class SubscribeForm(forms.ModelForm):
    link = forms.CharField(max_length=200, required=False)
    class Meta:
        model = subsData
        fields = ['link', 'date']
        exclude = ['date']
        widgets = {
            'date': forms.DateTimeInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        link_value = self.data.get('link')
        if link_value and link_value.strip() == '':
            self.data['link'] = ''
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['link'].required = False  # link 필드를 선택 사항으로 설정

class ScrapForm(forms.ModelForm):
    link = forms.URLField()
    title = forms.CharField(max_length=200)
    class Meta:
        model = scrapData
        fields = ['title', 'link']