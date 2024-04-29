from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from ..middleware import ThemeMiddleware
#from unittest.mock import patch, MagicMock
#from ..models import Profile

class ThemeMiddlewareTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = ThemeMiddleware(get_response=lambda request: 'response')
        self.user = User.objects.create_user(username='user', password='pass')
    
    def test_unauthenticated_user_theme(self):
        # Create an unauthenticated request
        request = self.factory.get('/some-url')
        request.user = AnonymousUser()

        # Apply middleware
        self.middleware(request)

        # Check theme is set to default
        self.assertEqual(request.theme, 'light')
        

'''    @patch('Profile.objects.get_or_create')
    def test_authenticated_user_theme(self, mock_get_or_create):
        # Set up mock
        profile_mock = MagicMock()
        profile_mock.dark_mode = False
        mock_get_or_create.return_value = (profile_mock, True)
        print("Mock successful")
        
        # Create an authenticated request
        request = self.factory.get('/some-url')
        request.user = self.user
        print("Request authenticated")

        # Apply middleware
        self.middleware(request)
        
        # Check theme setting based on user's profile
        self.assertEqual(request.theme, 'light')  # Code to possibly test authenticated Users in the future.'''




