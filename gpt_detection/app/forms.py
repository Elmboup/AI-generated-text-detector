from django import forms

class DetectionForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'style': 'width: 600px; height: 400px;'}))
    file = forms.FileField(required=False)