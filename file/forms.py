from django import forms
from .models import CSVfiles

class CSVForm(forms.ModelForm):
    class Meta:
        model = CSVfiles
        fields = ['file']

class CSVUpdateForm(forms.Form):
    row_data = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), required=False)
    column_name = forms.CharField(max_length=100, required=False)