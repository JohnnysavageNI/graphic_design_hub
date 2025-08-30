from django import forms
from django.test import TestCase
from django.contrib.auth import get_user_model
from services.models import Service
from orders.models import DesignRequest, Order
from orders.forms import CheckoutForm

User = get_user_model()


class TestDesignRequestForm(forms.ModelForm):
    class Meta:
        model = DesignRequest
        fields = ['instructions']


class DesignRequestFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='formuser', password='test'
        )
        self.service = Service.objects.create(
            name="Poster Design",
            description="Eye-catching poster",
            price=55.00,
            stripe_price_id="price_abc"
        )

    def test_valid_form(self):
        form_data = {'instructions': 'Include bold colors.'}
        form = TestDesignRequestForm(data=form_data)
        form.instance.user = self.user
        form.instance.service = self.service
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_instructions(self):
        form_data = {'instructions': ''}
        form = TestDesignRequestForm(data=form_data)
        form.instance.user = self.user
        form.instance.service = self.service
        self.assertFalse(form.is_valid())
        self.assertIn('instructions', form.errors)


class CheckoutFormTests(TestCase):
    def test_valid_checkout_form(self):
        form_data = {
            'full_name': 'Jane Doe',
            'email': 'jane@example.com',
            'instructions': 'Keep it simple.',
        }
        form = CheckoutForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_missing_email_allowed(self):
        form_data = {
            'full_name': 'Jane Doe',
            'email': '',
            'instructions': 'Simple layout please.',
        }
        form = CheckoutForm(data=form_data)
        self.assertTrue(form.is_valid())
