from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from ..tasks import collect_data
from django.conf import settings

class ViewTests(TestCase):
    @patch('tasks.collect_data')
    def test_landing_page(self, mock_collect):
        response = self.client.get(reverse('landing_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing_page.html')
        mock_collect.assert_called_once_with(
            settings.DROPOFF_DIR.resolve().as_posix(),
            settings.PSEUDO_DIR.resolve().as_posix(),
            settings.combined_glob_expression
        )

    def test_impressum(self):
        response = self.client.get(reverse('impressum'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about/impressum.html')

    def test_about_us(self):
        response = self.client.get(reverse('about_us'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about/about_us.html')

    def test_coloreg_security_concept(self):
        response = self.client.get(reverse('coloreg_security_concept'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'coloreg/security_concept.html')

    def test_help_page(self):
        response = self.client.get(reverse('help_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'help.html')

    def test_hdd_management(self):
        response = self.client.get(reverse('hdd_management'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'data_collector/hdd_management.html')
        self.assertEqual(response.context['partition_dict'], settings.PARTITION_DICT)
