from django import forms


class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    widget = MultiFileInput

    def clean(self, data, initial=None):
        if not data:
            return []
        if not isinstance(data, (list, tuple)):
            data = [data]
        cleaned = []
        single = forms.FileField(
            required=self.required,
            validators=self.validators,
        )
        for f in data:
            cleaned.append(single.clean(f, initial))
        return cleaned


class CheckoutForm(forms.Form):
    full_name = forms.CharField(
        max_length=100,
        required=False,
        label="Full name",
    )
    email = forms.EmailField(
        required=False,
        label="Email",
    )
    instructions = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 4}),
        required=True,
        label="Instructions for the designer",
    )
    uploaded_files = MultipleFileField(
        required=False,
        widget=MultiFileInput(attrs={"multiple": True}),
        label="Attach files (you can select multiple)",
    )
