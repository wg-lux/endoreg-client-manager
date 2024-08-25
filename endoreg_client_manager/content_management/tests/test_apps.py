from django.test import TestCase
from ..apps import ContentManagementConfig


class ThemeMiddlewareTest(TestCase):

    def test_unauthenticated_user_theme(self):

        self.assertEqual(ContentManagementConfig.name, 'content_management')
        self.assertEqual(ContentManagementConfig.default_auto_field, 'django.db.models.BigAutoField')
        



