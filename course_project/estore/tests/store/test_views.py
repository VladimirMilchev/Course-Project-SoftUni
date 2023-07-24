from django.http import HttpRequest
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from estore.store.views import product_all
from estore.store.models import Product, Category
from unittest import skip


class TestViewResponses(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.category = Category.objects.create(name='django', slug='django')
        self.user = User.objects.create(username='admin')
        self.data1 = Product.objects.create(category=self.category, title='django beginners', created_by=self.user,
                                            slug='django-beginners', price='20.00', image='django')

    def test_url_allowed_hosts(self):
        """
        Test allowed hosts
        """

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):
        """
        Test Product response status
        """

        response = self.client.get(reverse('estore:product detail', args=[self.data1.slug]))
        self.assertEqual(response.status_code, 200)

    def test_category_detail_url(self):
        """
        Test Category response status
        """

        response = self.client.get(reverse('estore:category list', args=[self.data1.category.slug]))
        self.assertEqual(response.status_code, 200)

    def test_homepage_html(self):
        """
        Test homepage response status
        """

        request = HttpRequest()
        response = product_all(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>BookStore</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)

    def test_view_function(self):
        """
        Test view function
        """

        request = self.factory.get('/django-beginners')
        response = product_all(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>BookStore</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)
