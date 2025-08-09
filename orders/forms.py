from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import DesignRequest


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = DesignRequest
        fields = ['full_name', 'email', 'instructions', 'uploaded_file']
        widgets = {
            'instructions': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Describe your brief...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_show_labels = True
        self.helper.add_input(Submit('submit', 'Pay securely'))
