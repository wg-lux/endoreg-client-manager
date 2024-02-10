from django.shortcuts import redirect, render

from logging import getLogger
logger = getLogger("my_oidc_backend")

# Create your views here.
def landing_page(request):
    # from django.contrib.sessions.models import Session
    # all_sessions = Session.objects.all()
    # logger.warning("REMOVING All Sessions:")

    # for session in all_sessions:
    #     logger.warning(session.get_decoded())
    #     session.delete()
    return render(request, "landing_page.html")

# views.py

from django.shortcuts import redirect
from .models import Profile

def toggle_dark_mode(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        profile.dark_mode = not profile.dark_mode
        profile.save()
    return redirect('')


def impressum(request):
    return render(request, "about/impressum.html")

def about_us(request):
    return render(request, "about/about_us.html")

def coloreg_security_concept(request):
    return render(request, "coloreg/security_concept.html")