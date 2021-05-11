from django import forms


class LocationForm(forms.Form):
    label = forms.CharField(label='Label')
    path = forms.CharField(label='Path')
