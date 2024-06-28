from django.contrib import admin 
from django.urls import path , include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import PredictEmissionView

urlpatterns = [
    path("" , views.index),
    path('api/predict-emission/', PredictEmissionView.as_view(), name='predict-emission'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)