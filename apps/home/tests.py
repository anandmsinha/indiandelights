from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from .models import Cities, Vendors, Taste, UnitType, Categories, Item
from django.core.files.uploadedfile import SimpleUploadedFile

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


class ViewsTestCase(TestCase):

    def test_home_page_is_working(self):
        response = self.client.get(reverse('home_page'))
        self.assertEqual(response.status_code, 200)

    def test_terms_page_is_working(self):
        response = self.client.get(reverse('site_terms'))
        self.assertEqual(response.status_code, 200)


class ModelsTestCase(TestCase):

    def setUp(self):
        self.city = Cities.objects.create(name='Bangalore')
        self.city2 = Cities.objects.create(name='Punjab')
        self.user = User.objects.create_user('anandms91@gmail.com', '12345678')
        self.vendor = Vendors.objects.create(name='Bakery house',
                                             city=self.city, user=self.user)
        self.vendor.delivers_in.add(self.city, self.city2)
        self.taste = Taste.objects.create(type='Sweet')
        self.unit_type = UnitType.objects.create(display_name='Kg')
        self.category = Categories.objects.create(name='Paan wala')
        self.uploaded_file = SimpleUploadedFile('x.jpg', 'a file')
        self.item = Item.objects.create(
            name='Petha', vendor=self.vendor, taste=self.taste, unit=self.unit_type,
            image=self.uploaded_file)

    def test_city_model(self):
        self.assertEqual(self.city.name, 'Bangalore')

    def test_vendor_model(self):
        self.assertEqual(self.vendor.city.name, self.city.name)
        self.assertEqual(
            self.vendor.get_delivery_cities(), 'Bangalore, Punjab')

    def test_item_model(self):
        self.assertEqual('<span class="text-success">In stock</span>', self.item.get_availability_message())

    def tearDown(self):
        self.item.delete()
