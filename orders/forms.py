from django import forms

class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=120)
    email = forms.EmailField()
    instructions = forms.CharField(widget=forms.Textarea(attrs={"rows": 5}), required=False)
    files = forms.FileField(
        widget=MultiFileInput(attrs={"multiple": True}),
        required=False,
        help_text="You can attach multiple files."
    )
