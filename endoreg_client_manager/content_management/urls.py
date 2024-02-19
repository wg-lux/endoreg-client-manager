# content_manatement/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing_page, name="landing_page"),

    # ColoReg
    path("coloreg/security-concept/", views.coloreg_security_concept, name="coloreg_security_concept"),

    # Help
    path('help/', views.help_page, name='help_page'),

    # About
    path("about/impressum/", views.impressum, name="impressum"),
    path("about/about-us/", views.about_us, name="about_us"),
]


