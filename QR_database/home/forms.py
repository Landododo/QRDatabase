from django import forms


class UploadGDSFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
    def clean_file(self):
        file = self.cleaned_data.get("file")
        if not file.name.endswith(".gds"):
            raise forms.ValidationError("Only GDS files are allowed.")
        return file

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class FileFieldForm(forms.Form):
    file_field = MultipleFileField()