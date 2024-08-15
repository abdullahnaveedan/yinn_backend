from django.contrib import admin 
from django.urls import path , include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import PredictEmissionView , DigitalProductAPIView

urlpatterns = [
    path("" , views.index),
    path('api/predict-emission/', PredictEmissionView.as_view(), name='predict-emission'),
    path('api/digital-products/', DigitalProductAPIView.as_view(), name='digital-products-api'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)