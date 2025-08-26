from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth import get_user_model
from .models import Profile
from orders.models import DesignRequest


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["full_name"]


class CustomSignupForm(SignupForm):
    full_name = forms.CharField(max_length=120, required=False, label="Full name")

    def save(self, request):
        user = super().save(request)
        profile, _ = Profile.objects.get_or_create(user=user)
        profile.full_name = self.cleaned_data.get("full_name", "").strip()
        profile.save()
        return user
    

class DesignRequestEditForm(forms.ModelForm):
    class Meta:
        model = DesignRequest
        fields = ["instructions"]
        widgets = {
            "instructions": forms.Textarea(attrs={"rows": 5, "class": "form-control"})
        }
