from django.test import TestCase
from django.apps import apps
from ..apps import VideoProcessorConfig

class VideoProcessorConfigTest(TestCase):
    def test_apps_config(self):
        # Ensure that the AppConfig name is correct
        self.assertEqual(VideoProcessorConfig.name, 'video_processor')
        self.assertEqual(apps.get_app_config('video_processor').name, 'video_processor')

        # Verify that the default auto field is set as expected
        self.assertEqual(apps.get_app_config('video_processor').default_auto_field, 'django.db.models.BigAutoField')

