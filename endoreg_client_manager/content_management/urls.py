# content_manatement/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing_page, name="landing_page"),
    path("about/impressum/", views.impressum, name="impressum"),
    path("about/about-us/", views.about_us, name="about_us"),

    path("coloreg/security-concept/", views.coloreg_security_concept, name="coloreg_security_concept"),
]


