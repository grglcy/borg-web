from django import forms


class ArchiveForm(forms.Form):
    label = forms.CharField(label='Label')
    fingerprint = forms.CharField(label='Fingerprint')
    name = forms.CharField(label='Name')
    start = forms.DateTimeField(label='Start', input_formats=["%Y-%m-%dT%H:%M:%S.%z"])
    end = forms.DateTimeField(label='End', input_formats=["%Y-%m-%dT%H:%M:%S.%z"])
    file_count = forms.IntegerField(label='File Count', min_value=0)
    original_size = forms.IntegerField(label='Original Size', min_value=0)
    compressed_size = forms.IntegerField(label='Compressed Size', min_value=0)
    deduplicated_size = forms.IntegerField(label='Deduplicated Size', min_value=0)

    total_chunks = forms.IntegerField(label='Total Chunks', min_value=0)
    total_csize = forms.IntegerField(label='Total Compressed Size', min_value=0)
    total_size = forms.IntegerField(label='Total Size', min_value=0)
    total_unique_chunks = forms.IntegerField(label='Total Unique Chunks', min_value=0)
    unique_csize = forms.IntegerField(label='Unique Size', min_value=0)
    unique_size = forms.IntegerField(label='Unique Compressed Size', min_value=0)
