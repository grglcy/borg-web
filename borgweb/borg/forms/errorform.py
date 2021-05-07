from django import forms


class ErrorForm(forms.Form):
    label = forms.CharField(label='Label')
    error = forms.CharField(label='Fingerprint')
    time = forms.DateTimeField(label='Last Modified', input_formats=["%Y-%m-%dT%H:%M:%S.%z"])
