from django.shortcuts import redirect, render
from .tasks import collect_data
import logging
# import django settings
from django.conf import settings
from endoreg_client_manager.settings import (
    DROPOFF_DIR,
    PSEUDO_DIR,
    PROCESSED_DIR,
    combined_glob_expression
)


logger = logging.getLogger("filepaths")
# log all paths


logger.info(f"DROPOFF_DIR: {DROPOFF_DIR}")
logger.info(f"PSEUDO_DIR: {PSEUDO_DIR}")
logger.info(f"PROCESSED_DIR: {PROCESSED_DIR}")

logger.info(f"combined_glob_expression: {combined_glob_expression}")

def landing_page(request):
    # from django.contrib.sessions.models import Session
    # all_sessions = Session.objects.all()
    # logger.warning("REMOVING All Sessions:")

    # for session in all_sessions:
    #     logger.warning(session.get_decoded())
    #     session.delete()
    dropoff_dir = DROPOFF_DIR.resolve().as_posix()
    pseudo_dir = PSEUDO_DIR.resolve().as_posix()
    collect_data(dropoff_dir, pseudo_dir, combined_glob_expression)
    return render(request, "landing_page.html")

# views.py

from django.shortcuts import redirect
# from .models import Profile

# def toggle_dark_mode(request):
#     if request.user.is_authenticated:
#         profile = Profile.objects.get(user=request.user)
#         profile.dark_mode = not profile.dark_mode
#         profile.save()
#     return redirect('')


def impressum(request):
    return render(request, "about/impressum.html")

def about_us(request):
    return render(request, "about/about_us.html")

def coloreg_security_concept(request):
    return render(request, "coloreg/security_concept.html")

def help_page(request):
    return render(request, 'help.html')

def hdd_management(request):
    context = {
        "partition_dict": settings.PARTITION_DICT
    }
    return render(request, 'data_collector/hdd_management.html', context)