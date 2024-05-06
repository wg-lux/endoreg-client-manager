from django.test import TestCase
from django.apps import apps
from ..apps import ReportProcessorConfig

class ReportProcessorConfigTest(TestCase):
    def test_apps_config_test(self):
        print(dir(ReportProcessorConfig))  # This will print all attributes and methods
        self.assertEqual(ReportProcessorConfig.name, 'report_processor')
    def test_apps_config(self):
        # Ensure that the AppConfig name is correct
        self.assertEqual(ReportProcessorConfig.name, 'report_processor')
        self.assertEqual(apps.get_app_config('report_processor').name, 'report_processor')

        # Verify that the default auto field is set as expected
        self.assertEqual(apps.get_app_config('report_processor').default_auto_field, 'django.db.models.BigAutoField')
