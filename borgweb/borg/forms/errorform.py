from django import forms


class ErrorForm(forms.Form):
    label = forms.CharField(label='Label')
    error = forms.CharField(label='Error')
    time = forms.DateTimeField(label='Time', input_formats=["%Y-%m-%dT%H:%M:%S.%z"])
