from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from estore.store.models import Category, Product


class TestBasketView(TestCase):
    def setUp(self):
        user = User.objects.create(username='admin')
        category = Category.objects.create(name='django', slug='django')
        self.product1 = Product.objects.create(category=category, title='django beginners', created_by=user,
                                               slug='django-beginners', price='20.00', image='django')
        self.product2 = Product.objects.create(category=category, title='django intermediate', created_by=user,
                                               slug='django-beginners', price='20.00', image='django')
        self.product3 = Product.objects.create(category=category, title='django advanced', created_by=user,
                                               slug='django-beginners', price='20.00', image='django')
        self.client.post(
            reverse('basket:basket add'), {"productid": self.product1.id, "productqty": 1, "action": "post"}, xhr=True)
        self.client.post(
            reverse('basket:basket add'), {"productid": self.product2.id, "productqty": 2, "action": "post"}, xhr=True)

    def test_basket_url(self):
        """
        Test homepage response status
        """
        response = self.client.get(reverse('basket:basket summary'))
        self.assertEqual(response.status_code, 200)

    def test_basket_add(self):
        """
        Test adding items to the basket
        """
        response = self.client.post(
            reverse('basket:basket add'), {"productid": self.product3.id, "productqty": 1, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 4})
        response = self.client.post(
            reverse('basket:basket add'), {"productid": self.product2.id, "productqty": 1, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 3})

    def test_basket_delete(self):
        """
        Test deleting items from the basket
        """
        response = self.client.post(
            reverse('basket:basket delete'), {"productid": self.product2.id, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 1, 'subtotal': '20.00'})

    def test_basket_update(self):
        """
        Test updating items in the basket
        """
        response = self.client.post(
            reverse('basket:basket update'), {"productid": self.product2.id, "productqty": 1, "action": "post"},
            xhr=True)
        self.assertEqual(response.json(), {'qty': 2, 'subtotal': '40.00'})
