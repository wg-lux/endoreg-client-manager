# middleware.py

# from .models import Profile

class ThemeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            # profile, created = Profile.objects.get_or_create(user=request.user)
            # request.theme = 'dark' if profile.dark_mode else 'light'
            request.theme = 'light'
        else:
            request.theme = 'light'
        return response
