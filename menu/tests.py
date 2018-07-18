from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import *
import random

class MenuTestCase(TestCase):
    fixtures = ['menu']

    def setUp(self):
        count = len(Menu.objects.all())
        pk = round(random.randint(0, count))
        self.menu = Menu.objects.get(pk=pk)

    def test_detail(self):
        res = self.client.get(reverse('menu_detail', kwargs={'pk': self.menu.pk}))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.menu.season)