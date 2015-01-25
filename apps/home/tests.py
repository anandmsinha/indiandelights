import os
import sys

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

from .models import Cities, Vendors, Taste, UnitType, Categories, Item, HomePage


User = get_user_model()


class AuthModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('anandms91@gmail.com', '12345678')
        self.admin = User.objects.create_superuser('ams@gmail.com', '0000')

    def test_model_is_working(self):
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_superuser)

    def test_superuser_is_working(self):
        self.assertTrue(self.admin.is_superuser)

    def tearDown(self):
        self.user.delete()
        self.admin.delete()


class AppTestCase(TestCase):

    def setUp(self):
        TEST_ROOT = os.path.abspath(os.path.dirname(__file__))
        self._old_media_root = settings.MEDIA_ROOT
        settings.MEDIA_ROOT = os.path.join(TEST_ROOT, '../testdata/media/')
        self.image_file = file(
            settings.MEDIA_ROOT + 'Food-Products-Bangalore-Ooty-Chocolates-1aibhzml-4f338cc8861e6_regular.jpg')
        self.uploadedfile = SimpleUploadedFile(self.image_file.name, self.image_file.read())

        self.user = User.objects.create_user('anandms91@gmail.com', '12345678')
        Cities.objects.bulk_create([
            Cities(name='punjab'),
            Cities(name='Bangalore'),
            Cities(name='New Delhi')
        ])
        self.cities = Cities.objects.all()
        Vendors.objects.bulk_create([
            Vendors(name='vendora', city=self.cities[0], user=self.user),
            Vendors(name='vendorb', city=self.cities[0], user=self.user)
        ])
        self.vendors = Vendors.objects.all()
        self.vendors[0].delivers_in.add(self.cities[0], self.cities[1])
        self.vendors[1].delivers_in.add(self.cities[0], self.cities[1])
        self.taste = Taste.objects.create(type='Sweet')
        self.unit_type = UnitType.objects.create(display_name='1 Kg')
        self.unity_type_piece = UnitType.objects.create(display_name='16 pieces', weight=False, piece=True)
        self.category = Categories.objects.create(name='Ooty choclates')
        self.item = Item.objects.create(name='itema', vendor=self.vendors[0], taste=self.taste, unit=self.unit_type, image=self.uploadedfile)
        self.item.categories.add(self.category)
        self.item_piece = Item.objects.create(name='itemb', vendor=self.vendors[0], taste=self.taste, unit=self.unity_type_piece, image=self.uploadedfile)
        self.item_piece.categories.add(self.category)
        self.home_page = HomePage.objects.create(category=self.category)
        self.home_page.decode_json()
        self.home_page_test = HomePage.objects.create(category=self.category, metadata='{"label": "sample", "grids": 8}')
        self.home_page_test.decode_json()

    def test_vendors_model(self):
        ''' Cities cocatenation of vendor should word properly '''
        self.assertEqual(self.vendors[0].get_delivery_cities(), 'punjab, Bangalore')

    def test_items_model(self):
        self.assertEqual(self.item.get_availability_message(), '<span class="text-success">In stock</span>')

    def test_home_page_model(self):
        self.assertEqual(self.home_page.get_page_limit(), 6)
        self.assertEqual(self.home_page_test.get_page_limit(), 8)
        self.assertEqual(self.home_page.get_label(), self.category.name)
        self.assertEqual(self.home_page_test.get_label(), 'sample')

    def test_home_page_view(self):
        response = self.client.get(reverse('home_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('home_components' in response.context)
        self.assertTrue('slider_images' in response.context)
        self.assertTrue('loop_range' in response.context)
        self.assertNotEqual(len(response.context['home_components']), 0)

    def test_all_vendors_view(self):
        response = self.client.get(reverse('vendor_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('vendors' in response.context)
        self.assertNotEqual(len(response.context['vendors']), 0)

    def tearDown(self):
        settings.MEDIA_ROOT = self._old_media_root
