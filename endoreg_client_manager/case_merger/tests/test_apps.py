from django.test import TestCase
from ..apps import CaseMergerConfig


class ThemeMiddlewareTest(TestCase):

    def test_unauthenticated_user_theme(self):

        self.assertEqual(CaseMergerConfig.name, 'case_merger')
        self.assertEqual(CaseMergerConfig.default_auto_field, 'django.db.models.BigAutoField')
        



