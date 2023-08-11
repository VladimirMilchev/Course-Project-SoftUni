from django.test import TestCase
from django.urls import reverse
from estore.apps.catalogue.models import ProductType, Category, Product


class TestBasketView(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Test Category")
        product_type = ProductType.objects.create(name="Test Product Type")
        self.product1 = Product.objects.create(title="Test Product1", regular_price=10.00, discount_price=8.00,
                                               category=category, product_type=product_type)
        self.product2 = Product.objects.create(title="Test Product2", regular_price=11.00, discount_price=9.00,
                                               category=category, product_type=product_type)
        self.product3 = Product.objects.create(title="Test Product3", regular_price=12.00, discount_price=10.00,
                                               category=category, product_type=product_type)
        self.client.post(
            reverse('basket:basket_add'), {"productid": self.product1.id, "productqty": 1, "action": "post"}, xhr=True)
        self.client.post(
            reverse('basket:basket_add'), {"productid": self.product2.id, "productqty": 2, "action": "post"}, xhr=True)

    def test_basket_url(self):
        """
        Test homepage response status
        """
        response = self.client.get(reverse('basket:basket_summary'))
        self.assertEqual(response.status_code, 200)

    def test_basket_add(self):
        """
        Test adding items to the basket
        """
        response = self.client.post(
            reverse('basket:basket_add'), {"productid": self.product3.id, "productqty": 1, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 4})
        response = self.client.post(
            reverse('basket:basket_add'), {"productid": self.product2.id, "productqty": 1, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 3})

    def test_basket_delete(self):
        """
        Test deleting items from the basket
        """
        response = self.client.post(
            reverse('basket:basket_delete'), {"productid": self.product2.id, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 1, 'subtotal': '10.00'})

    def test_basket_update(self):
        """
        Test updating items in the basket
        """
        response = self.client.post(
            reverse('basket:basket_update'), {"productid": self.product2.id, "productqty": 1, "action": "post"},
            xhr=True)
        self.assertEqual(response.json(), {'qty': 2, 'subtotal': '21.00'})