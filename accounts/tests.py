from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import Profile

User = get_user_model()


class RegistrationLoginTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('account_signup')
        self.login_url = reverse('account_login')

    def test_user_can_register(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'email2': 'newuser@example.com',
            'password1': 'SuperStrongPass123!',
            'password2': 'SuperStrongPass123!',
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_can_login(self):
        User.objects.create_user(
            username='loginuser',
            password='securepass123'
        )
        response = self.client.post(self.login_url, {
            'login': 'loginuser',
            'password': 'securepass123',
        })
        self.assertEqual(response.status_code, 302)


class ProfileModelTests(TestCase):
    def test_profile_str_returns_name(self):
        user = User.objects.create_user(
            username='profileuser',
            password='pass'
        )
        user.profile.full_name = 'John Doe'
        user.profile.save()
        self.assertEqual(str(user.profile), 'John Doe')

        user = User.objects.create_user(
            username='fallbackuser',
            password='pass'
        )
        self.assertEqual(str(user.profile), 'fallbackuser')
        self.assertEqual(str(user.profile), 'fallbackuser')
