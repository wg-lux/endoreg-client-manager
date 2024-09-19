"""
URL configuration for endoreg_client_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from endoreg_db.forms import TtoQuestionnaireCreate
from .views import SaveDataView, ValidateAndSaveView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/data_collector/', include('data_collector.urls')),
    path('', include('content_management.urls')),
    path("tto_questionnaire/", TtoQuestionnaireCreate.as_view(), name="tto_questionnaire"),
    path("save-data/", SaveDataView.as_view(), name="save_data"),
    path("validate-and-save/", ValidateAndSaveView.as_view(), name="validate_and_save"),
    #path("anonymization-request/", AnonymizationRequestView.as_view(), name="anonymization_request"),
    #path("handle-annotation/", HandleAnnotationView.as_view(), name="handle_annotation"),
]



# While WhiteNoise is excellent for static files, Django recommends against 
# serving media files (like uploaded videos) in a production environment. 
# In development, you can add the following to your urls.py to serve media files:
from django.conf import settings
from django.conf.urls.static import static

# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

