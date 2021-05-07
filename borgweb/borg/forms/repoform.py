from django import forms


class RepoForm(forms.Form):
    label = forms.CharField(label='Label')
    fingerprint = forms.CharField(label='Fingerprint')
    location = forms.CharField(label='Location')
    last_modified = forms.DateTimeField(label='Last Modified', input_formats=["%Y-%m-%dT%H:%M:%S.%z"])
