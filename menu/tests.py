from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import *
import random

class MenuTestCase(TestCase):
    """Tests all things around menus"""
    fixtures = ['menu']

    def setUp(self):
        """Setup testing enviroment"""
        # Get a random menu to perform tests with
        count = len(Menu.objects.all())
        pk = round(random.randint(0, count))
        self.menu = Menu.objects.get(pk=pk)

    def test_detail(self):
        """Test the menu detail page"""
        res = self.client.get(reverse('menu_detail', kwargs={'pk': self.menu.pk}))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.menu)

    def test_home(self):
        """Test the home page"""
        res = self.client.get(reverse('menu_list'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.menu)

    def test_item_detail(self):
        """Test the item detail page"""
        res = self.client.get(reverse('item_detail', kwargs={'pk': self.menu.items.first().pk}))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.menu.items.first().name)