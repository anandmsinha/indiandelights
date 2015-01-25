from django.test import TestCase
from django.core.urlresolvers import reverse
from apps.home.models import Item


class ProductTestCase(TestCase):

    def setUp(self):
        self.items = Item.objects.all()

    def test_cart_manager_view(self):
        response = self.client.post(reverse('cart_view'), {'type': 'add', 'pid': self.items[0].pk, 'quantity': 1})
        self.assertEqual(response.status_code, 200)