from django.test import TestCase
from ..apps import DataCollectorConfig


class ThemeMiddlewareTest(TestCase):

    def test_unauthenticated_user_theme(self):

        self.assertEqual(DataCollectorConfig.name, 'data_collector')
        self.assertEqual(DataCollectorConfig.default_auto_field, 'django.db.models.BigAutoField')
        



