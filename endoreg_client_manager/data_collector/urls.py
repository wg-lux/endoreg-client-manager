# data_collector/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# router = DefaultRouter()
# router.register(r'rawfile', views.YourModelViewSet)

urlpatterns = [
    # path('', include(router.urls)),
]
