from django.test import TestCase, Client
from django.urls import reverse


class HomePageViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('home')

    def test_homepage_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_homepage_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'home/index.html')

    def test_homepage_content(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'Design')
