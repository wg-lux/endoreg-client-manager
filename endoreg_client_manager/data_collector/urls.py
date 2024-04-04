# data_collector/urls.py

from django.urls import path, include
from . import views

# router = DefaultRouter()
# router.register(r'rawfile', views.YourModelViewSet)

urlpatterns = [
    path('mount/<str:partition_name>/', views.mount_partition_view, name='mount_partition'),
    path('unmount/<str:partition_name>/', views.unmount_partition_view, name='unmount_partition'),
    path("check_mount_status/", views.check_mount_status, name="check_mount_status"),
]
