# data_collector/urls.py

from django.urls import path, include
from . import views

# router = DefaultRouter()
# router.register(r'rawfile', views.YourModelViewSet)

urlpatterns = [
    path('mount/<str:partition_name>/', views.mount_partition_view, name='mount_partition'),
    path('unmount/<str:partition_name>/', views.unmount_partition_view, name='unmount_partition'),
    path("check_mount_status/", views.check_mount_status, name="check_mount_status"),
    path("api/save_data/", views.SaveData.as_view(), name="save_data"),
    path('api/', include('rest_framework.urls', namespace='rest_framework')),
    path("api/anonymized_file/", views.AnonymizedFileListCreate.as_view(), name="anonymized_file_list_create"),
    path("api/annotations/", views.AnnotationListCreate.as_view(), name="annotation_list_create"),
]
